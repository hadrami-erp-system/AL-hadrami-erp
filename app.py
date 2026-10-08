# ====================================================================
# ⚜️ نظام الحضرمي المتكامل لإدارة موارد المؤسسات - طبعة الإقلاع النهائي 2026 ⚜️
# ====================================================================

import streamlit as st
import pandas as pd
import sqlite3
import os
import tempfile
from datetime import datetime
import qrcode
from io import BytesIO
import base64

# ====== إعدادات Streamlit ======
st.set_page_config(
    page_title="🏢 نظام الحضرمي ERP 2026",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====== إدارة الملفات في السحابة ======
TEMP_DIR = tempfile.gettempdir()
DB_FILE = os.path.join(TEMP_DIR, "al_hadrami_sky_production.db")
ATTACH_DIR = os.path.join(TEMP_DIR, "attachments")
BACKUP_DIR = os.path.join(TEMP_DIR, "backups")

for directory in [ATTACH_DIR, BACKUP_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# ====== Cache للبيانات ======
@st.cache_resource
def get_db_connection():
    """الاتصال بقاعدة البيانات"""
    return sqlite3.connect(DB_FILE, check_same_thread=False)

@st.cache_data
def load_privileges():
    """تحميل البيانات المخزنة مؤقتاً"""
    conn = get_db_connection()
    return pd.read_sql_query("SELECT * FROM system_privileges", conn)

def generate_zatca_qr(seller_name, vat_reg_num, timestamp, total_amt, vat_amt):
    """توليد رمز QR لـ ZATCA"""
    try:
        qr_data = f"{seller_name}|{vat_reg_num}|{timestamp}|{total_amt}|{vat_amt}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    except Exception as e:
        return None

def init_database():
    """تهيئة قاعدة البيانات"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # جدول المستندات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS erp_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_type TEXT, status TEXT, date TEXT, doc_num TEXT,
        account_no TEXT, account_name TEXT, debit REAL, credit REAL,
        cost_center TEXT, client_name TEXT, description TEXT,
        financial_period TEXT, branch_name TEXT, currency_code TEXT DEFAULT 'SAR'
    )""")
    
    # جدول الموظفين والصلاحيات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_privileges (
        username TEXT PRIMARY KEY,
        display_name TEXT,
        user_role TEXT,
        account_status TEXT
    )""")
    
    # جدول بيانات الشركة
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS corporate_profile (
        id INTEGER PRIMARY KEY,
        comp_name TEXT,
        vat_number TEXT,
        address TEXT,
        postal_code TEXT,
        phone_no TEXT,
        email_address TEXT,
        bank_iban TEXT,
        notes TEXT,
        corporate_qr_enabled TEXT
    )""")
    
    # جدول المخزون
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_master_ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_code TEXT, item_name TEXT, quantity REAL,
        unit_cost REAL, total_value REAL, warehouse_name TEXT,
        created_at TEXT
    )""")
    
    # جدول دليل الحسابات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chart_of_accounts (
        account_no TEXT PRIMARY KEY,
        account_name TEXT,
        parent_no TEXT,
        account_type TEXT,
        financial_statement TEXT,
        depth_level INTEGER
    )""")
    
    # جدول سجل التدقيق
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_audit_trail_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operator_name TEXT,
        action_performed TEXT,
        document_referenced TEXT,
        timestamp_logged TEXT
    )""")
    
    # جدول الفترات المالية المغلقة
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locked_financial_periods (
        period_name TEXT PRIMARY KEY,
        is_locked TEXT
    )""")
    
    # جدول مراكز التكلفة
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS geo_analytic_cost_centers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch_name TEXT,
        main_cost_center TEXT,
        sub_cost_center_name TEXT
    )""")
    
    # جدول حدود الائتمان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client_credit_limits (
        client_name TEXT PRIMARY KEY,
        credit_limit REAL,
        current_balance REAL
    )""")
    
    conn.commit()
    
    # حقن البيانات الأولية
    cursor.execute("SELECT COUNT(*) FROM system_privileges")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO system_privileges VALUES (?, ?, ?, ?)",
            [
                ("owner", "المالك المطور للنظام 👑", "مالك النظام (Super Admin)", "مفعل ✅"),
                ("admin", "أستاذ أنور عمر", "مدير الشركة (Company Admin)", "مفعل ✅"),
                ("supervisor", "مشرف النظام", "مشرف (Supervisor)", "مفعل ✅")
            ]
        )
    
    cursor.execute("SELECT COUNT(*) FROM corporate_profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO corporate_profile VALUES 
        (1, 'مجموعة الحضرمي التجارية القابضة', '310961234567693',
        'الطائف - المملكة العربية السعودية', '21944', '+966127320000',
        'info@hadrami.com', 'SA8040000012345678901234',
        'الحسابات خاضعة للمعايير الدولية IFRS', 'نعم')
        """)
    
    cursor.execute("SELECT COUNT(*) FROM chart_of_accounts")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO chart_of_accounts VALUES (?, ?, ?, ?, ?, ?)",
            [
                ("120301", "الصندوق الرئيسي", "1203", "طفل", "الميزانية العمومية", 4),
                ("210302", "مخصص ضريبة القيمة المضافة", "2103", "طفل", "الميزانية العمومية", 4),
                ("4101", "إيرادات المبيعات", "41", "أب", "قائمة الدخل", 3),
                ("520301", "مصروفات المكتب", "5203", "طفل", "قائمة الدخل", 4)
            ]
        )
    
    cursor.execute("SELECT COUNT(*) FROM locked_financial_periods")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO locked_financial_periods VALUES (?, ?)",
            [("يناير 2026", "نعم"), ("فبراير 2026", "لا"), ("مارس 2026", "لا")]
        )
    
    cursor.execute("SELECT COUNT(*) FROM geo_analytic_cost_centers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO geo_analytic_cost_centers VALUES (NULL, ?, ?, ?)",
            [
                ("الطائف", "المقاولات", "أعمال الخرسانة"),
                ("الطائف", "التجاري", "مبيعات كاشير"),
                ("سيئون", "المقاولات", "أعمال التشطيبات")
            ]
        )
    
    cursor.execute("SELECT COUNT(*) FROM client_credit_limits")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO client_credit_limits VALUES (?, ?, ?)",
            [
                ("شركة الحضرمي للمقاولات", 150000.00, 45000.00),
                ("مبيعات نقدية", 9999999.00, 0.00)
            ]
        )
    
    conn.commit()

# تهيئة قاعدة البيانات
init_database()

# ====== CSS مخصص ======
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #5B1E31;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #5B1E31, #8B3A50);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .status-active {
        color: #2ecc71;
        font-weight: bold;
    }
    .status-inactive {
        color: #e74c3c;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ====== الرأس ======
st.markdown('<div class="main-title">⚜️ نظام الحضرمي ERP 2026 ⚜️</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">نظام إدارة موارد المؤسسات المتكامل - الطبعة السحابية</div>', unsafe_allow_html=True)
st.markdown("---")

# ====== القائمة الجانبية ======
with st.sidebar:
    st.title("🔐 القائمة الرئيسية")
    st.markdown("---")
    
    menu_selection = st.radio(
        "اختر القسم:",
        [
            "📊 لوحة المعلومات",
            "📄 المستندات",
            "💰 الحسابات",
            "📦 المخزون",
            "👥 الموظفون",
            "📋 الفترات المالية",
            "🏭 مراكز التكلفة",
            "⚙️ الإعدادات"
        ]
    )

# ====== المحتوى الرئيسي ======

if menu_selection == "📊 لوحة المعلومات":
    st.subheader("📊 لوحة معلومات النظام")
    
    conn = get_db_connection()
    
    # المقاييس
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        doc_count = pd.read_sql_query("SELECT COUNT(*) as count FROM erp_documents", conn).iloc[0, 0]
        st.metric("📄 المستندات", doc_count, "+0")
    
    with col2:
        inv_count = pd.read_sql_query("SELECT COUNT(*) as count FROM inventory_master_ledger", conn).iloc[0, 0]
        st.metric("📦 المخزون", inv_count, "+0")
    
    with col3:
        client_count = pd.read_sql_query("SELECT COUNT(*) as count FROM client_credit_limits", conn).iloc[0, 0]
        st.metric("👥 العملاء", client_count, "+0")
    
    with col4:
        user_count = pd.read_sql_query("SELECT COUNT(*) as count FROM system_privileges", conn).iloc[0, 0]
        st.metric("👤 الموظفون", user_count, "+0")
    
    st.markdown("---")
    
    # معلومات الشركة
    st.subheader("🏢 معلومات الشركة")
    comp = pd.read_sql_query("SELECT * FROM corporate_profile WHERE id=1", conn)
    if not comp.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**الاسم:** {comp['comp_name'].values[0]}")
            st.write(f"**رقم الضريبة:** {comp['vat_number'].values[0]}")
            st.write(f"**الهاتف:** {comp['phone_no'].values[0]}")
        with col2:
            st.write(f"**البريد:** {comp['email_address'].values[0]}")
            st.write(f"**العنوان:** {comp['address'].values[0]}")
            st.write(f"**IBAN:** {comp['bank_iban'].values[0]}")

elif menu_selection == "📄 المستندات":
    st.subheader("📄 إدارة المستندات")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ مستند جديد", use_container_width=True):
            st.session_state.show_doc_form = True
    
    conn = get_db_connection()
    
    if st.session_state.get('show_doc_form', False):
        with st.form("doc_form"):
            col1, col2 = st.columns(2)
            with col1:
                doc_type = st.selectbox("نوع المستند", ["فاتورة", "إيصال", "شيك", "طلب شراء"])
                doc_num = st.text_input("رقم المستند")
            with col2:
                status = st.selectbox("الحالة", ["جديد", "معلق", "مكتمل", "ملغى"])
                date = st.date_input("التاريخ")
            
            col1, col2 = st.columns(2)
            with col1:
                account_no = st.text_input("رقم الحساب")
                debit = st.number_input("مدين", min_value=0.0)
            with col2:
                account_name = st.text_input("اسم الحساب")
                credit = st.number_input("دائن", min_value=0.0)
            
            description = st.text_area("الوصف")
            
            if st.form_submit_button("💾 حفظ"):
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO erp_documents 
                    (doc_type, doc_num, status, date, account_no, account_name, debit, credit, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (doc_type, doc_num, status, str(date), account_no, account_name, debit, credit, description)
                )
                conn.commit()
                st.success("✅ تم حفظ المستند بنجاح!")
                st.session_state.show_doc_form = False
                st.rerun()
    
    # عرض المستندات
    docs_df = pd.read_sql_query(
        "SELECT doc_num, doc_type, status, date, account_name, debit, credit FROM erp_documents ORDER BY date DESC",
        conn
    )
    
    if not docs_df.empty:
        st.dataframe(docs_df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 لا توجد مستندات حالياً")

elif menu_selection == "💰 الحسابات":
    st.subheader("💰 دليل الحسابات")
    
    conn = get_db_connection()
    coa_df = pd.read_sql_query(
        "SELECT account_no, account_name, account_type, financial_statement FROM chart_of_accounts ORDER BY account_no",
        conn
    )
    
    if not coa_df.empty:
        st.dataframe(coa_df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 لا توجد حسابات")

elif menu_selection == "📦 المخزون":
    st.subheader("📦 إدارة المخزون")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ عنصر جديد", use_container_width=True):
            st.session_state.show_inv_form = True
    
    conn = get_db_connection()
    
    if st.session_state.get('show_inv_form', False):
        with st.form("inv_form"):
            col1, col2 = st.columns(2)
            with col1:
                item_code = st.text_input("كود العنصر")
                item_name = st.text_input("اسم العنصر")
            with col2:
                quantity = st.number_input("الكمية", min_value=0.0)
                unit_cost = st.number_input("سعر الوحدة", min_value=0.0)
            
            warehouse = st.text_input("المستودع")
            
            if st.form_submit_button("💾 حفظ"):
                cursor = conn.cursor()
                total_value = quantity * unit_cost
                cursor.execute(
                    """INSERT INTO inventory_master_ledger 
                    (item_code, item_name, quantity, unit_cost, total_value, warehouse_name, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (item_code, item_name, quantity, unit_cost, total_value, warehouse, str(datetime.now()))
                )
                conn.commit()
                st.success("✅ تم إضافة العنصر بنجاح!")
                st.session_state.show_inv_form = False
                st.rerun()
    
    inv_df = pd.read_sql_query(
        "SELECT item_code, item_name, quantity, unit_cost, total_value, warehouse_name FROM inventory_master_ledger",
        conn
    )
    
    if not inv_df.empty:
        st.dataframe(inv_df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 المخزن فارغ")

elif menu_selection == "👥 الموظفون":
    st.subheader("👥 إدارة الموظفين")
    
    conn = get_db_connection()
    priv_df = pd.read_sql_query(
        "SELECT username, display_name, user_role, account_status FROM system_privileges",
        conn
    )
    
    st.dataframe(priv_df, use_container_width=True, hide_index=True)

elif menu_selection == "📋 الفترات المالية":
    st.subheader("📋 الفترات المالية")
    
    conn = get_db_connection()
    periods_df = pd.read_sql_query(
        "SELECT period_name, is_locked FROM locked_financial_periods",
        conn
    )
    
    st.dataframe(periods_df, use_container_width=True, hide_index=True)

elif menu_selection == "🏭 مراكز التكلفة":
    st.subheader("🏭 مراكز التكلفة الجغرافية")
    
    conn = get_db_connection()
    geo_df = pd.read_sql_query(
        "SELECT branch_name, main_cost_center, sub_cost_center_name FROM geo_analytic_cost_centers",
        conn
    )
    
    if not geo_df.empty:
        st.dataframe(geo_df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 لا توجد مراكز تكلفة")

elif menu_selection == "⚙️ الإعدادات":
    st.subheader("⚙️ إعدادات النظام")
    
    tab1, tab2, tab3 = st.tabs(["🏢 بيانات الشركة", "📊 الإحصائيات", "🔧 الإجراءات"])
    
    conn = get_db_connection()
    
    with tab1:
        comp = pd.read_sql_query("SELECT * FROM corporate_profile WHERE id=1", conn)
        if not comp.empty:
            st.write(f"**اسم الشركة:** {comp['comp_name'].values[0]}")
            st.write(f"**رقم الضريبة:** {comp['vat_number'].values[0]}")
            st.write(f"**الهاتف:** {comp['phone_no'].values[0]}")
            st.write(f"**البريد:** {comp['email_address'].values[0]}")
            st.write(f"**العنوان:** {comp['address'].values[0]}")
            st.write(f"**الملاحظات:** {comp['notes'].values[0]}")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            doc_count = pd.read_sql_query("SELECT COUNT(*) as count FROM erp_documents", conn).iloc[0, 0]
            st.metric("إجمالي المستندات", doc_count)
        with col2:
            inv_count = pd.read_sql_query("SELECT COUNT(*) as count FROM inventory_master_ledger", conn).iloc[0, 0]
            st.metric("إجمالي عناصر المخزون", inv_count)
    
    with tab3:
        if st.button("🔄 إعادة تحميل البيانات"):
            st.cache_data.clear()
            st.success("✅ تم إعادة التحميل")
        
        if st.button("💾 تصدير البيانات (CSV)"):
            docs_df = pd.read_sql_query("SELECT * FROM erp_documents", conn)
            csv = docs_df.to_csv(index=False)
            st.download_button(
                label="📥 تحميل CSV",
                data=csv,
                file_name="erp_data.csv",
                mime="text/csv"
            )

# ====== الفوتر ======
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.85rem; margin-top: 2rem;">
    <p>© 2026 مجموعة الحضرمي التجارية القابضة | جميع الحقوق محفوظة</p>
    <p>نسخة تجريبية | الطبعة السحابية 2026</p>
    <p>📧 info@hadrami.com | ☎️ +966127320000</p>
</div>
""", unsafe_allow_html=True)
