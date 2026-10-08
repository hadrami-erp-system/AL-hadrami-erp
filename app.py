# ====================================================================
# ⚜️ نظام الحضرمي المتكامل لإدارة موارد المؤسسات - طبعة الإقلاع النهائي 2026 ⚜️
# 🛑 كود الصهر الكلي والمطهر 100% من أخطاء المسافات والفراغات البرمجية الجراحية
# ====================================================================

import streamlit as st
import pandas as pd
import sqlite3
import os
import io
import base64
import qrcode
import shutil
from datetime import datetime

# --------------------------------------------------------------------
# 📂 1. تأسيس قاعدة البيانات المركزية ومستودعات التخزين الهجينة
# --------------------------------------------------------------------
DB_FILE = "al_hadrami_sky_production.db"
ATTACH_DIR = "stored_system_attachments"
BACKUP_DIR = "local_hardware_backups"
if not os.path.exists(ATTACH_DIR): os.makedirs(ATTACH_DIR)
if not os.path.exists(BACKUP_DIR): os.makedirs(BACKUP_DIR)

def init_master_erp_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # أ) جدول وثائق الكيان خماسية الأبعاد
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS erp_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT, doc_type TEXT, status TEXT, date TEXT, doc_num TEXT, account_no TEXT, account_name TEXT,
        debit REAL, credit REAL, cost_center TEXT, sub_cost_center TEXT, client_name TEXT, description TEXT, attachment_path TEXT, financial_period TEXT, branch_name TEXT, currency_code TEXT DEFAULT 'SAR'
    )""")
    # ب) مصفوفة الصلاحيات وحوكمة رتب الموظفين والمالك
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_privileges (
        username TEXT PRIMARY KEY, display_name TEXT, user_role TEXT, account_status TEXT
    )""")
    # ج) بطاقة ومطبعة معلومات وتروية المنشأة للمدير
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS corporate_profile (
        id INTEGER PRIMARY KEY, comp_name TEXT, vat_number TEXT, address TEXT, postal_code TEXT, phone_no TEXT, email_address TEXT, bank_iban TEXT, notes TEXT, corporate_qr_enabled TEXT
    )""")
    # د) قوالب السمت والهندسة البصرية للواجهات والأزرار والخطوط للمالك
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_design_template (
        id INTEGER PRIMARY KEY, selected_template TEXT, font_family TEXT, font_size INTEGER, border_radius INTEGER, primary_color TEXT, system_rights TEXT
    )""")
    # هـ) مجمع حركة المخازن المركزي الموحد وحظر البيع بالسالب
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_master_ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT, item_code TEXT, item_name TEXT, target_sector TEXT, transaction_type TEXT, quantity REAL, unit_cost REAL, total_value REAL, warehouse_name TEXT, created_at TEXT
    )""")
    # و) شجرة الحسابات والدليل المحاسبي الديناميكي سداسي المستويات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chart_of_accounts (
        account_no TEXT PRIMARY KEY, account_name TEXT, parent_no TEXT, account_type TEXT, financial_statement TEXT, depth_level INTEGER
    )""")
    # ز) سجل التتبع الرقابي الصامت وفحص أمان العمليات والتحصين ضد الاختلاس
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_audit_trail_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, operator_name TEXT, action_performed TEXT, document_referenced TEXT, timestamp_logged TEXT
    )""")
    # ح) فترات الإقفال المالي السنوي وحجر الحركات بالفترات المغلقة
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locked_financial_periods (
        period_name TEXT PRIMARY KEY, is_locked TEXT
    )""")
    # ط) مصفوفة توزيع مراكز التكلفة الفرعية جغرافياً على مستوى كل فرع
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS geo_analytic_cost_centers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, branch_name TEXT, main_cost_center TEXT, sub_cost_center_name TEXT
    )""")
    # ي) درع حظر تجاوز الأسقف الائتمانية لعملاء مبيعات الآجل لحماية السيولة
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client_credit_limits (
        client_name TEXT PRIMARY KEY, credit_limit REAL, current_balance REAL
    )""")
    # ك) مصفوفة بطاقات باركود التجاوز الإداري للمشرفين والمسؤولين كالمولات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manager_override_keys (
        manager_name TEXT PRIMARY KEY, supervisor_barcode TEXT, pin_code TEXT
    )""")
    # ل) محرك أيام فترة السماح المتغيرة للأثر الرجعي والمحكوم من لوحة المالك
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dynamic_grace_period_config (
        id INTEGER PRIMARY KEY, allowed_grace_days INTEGER
    )""")
    # م) الأبعاد الهندسية لحجم وتحريك موقع ختم اسم البرنامج لحفظ حقوق المالك
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sovereign_rights_geometry (
        id INTEGER PRIMARY KEY, stamp_size INTEGER, stamp_position TEXT
    )""")
    
    conn.commit()
    
    # 🔒 مراجعة وحقن جراحي نظيف لكل حقول الـ IF والتأكد من تطابق المسافات بالمليمتر
    cursor.execute("SELECT COUNT(*) FROM dynamic_grace_period_config")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO dynamic_grace_period_config VALUES (1, 4)")
        
    cursor.execute("SELECT COUNT(*) FROM sovereign_rights_geometry")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO sovereign_rights_geometry VALUES (1, 10, 'top: 12px; left: 15px;')")
        
    cursor.execute("SELECT COUNT(*) FROM manager_override_keys")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO manager_override_keys VALUES (?, ?, ?)", [
            ("مالك النظام السيادي 👑", "OWNER-MASTER-KEY-2026", "1234"),
            ("الأستاذ أنور عمر (مدير عام المجموعة) 🔑", "HADRAMI-SUPERVISOR-2026", "9900"),
            ("مشرف فرع سيئون الإقليمي 📍", "SAYUN-SUPER-KEY-88", "8822")
        ])
        
    cursor.execute("SELECT COUNT(*) FROM locked_financial_periods")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO locked_financial_periods VALUES (?, ?)", [("يناير 2026", "نعم"), ("أكتوبر 2026", "لا"), ("نوفمبر 2026", "لا")])
        
    cursor.execute("SELECT COUNT(*) FROM geo_analytic_cost_centers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO geo_analytic_cost_centers VALUES (NULL, ?, ?, ?)", [
            ("المركز الرئيسي - الطائف", "قطاع المقاولات والمشاريع", "برج السليمانية - أعمال الخرسانة والأساسات"),
            ("المركز الرئيسي - الطائف", "القطاع التجاري والتجزئة", "معرض مبيعات كاشير نقاط البيع"),
            ("فرع سيئون الإقليمي", "قطاع المقاولات والمشاريع", "مشروع مستودعات الشحن - أعمال التشطيبات")
        ])
        
    cursor.execute("SELECT COUNT(*) FROM client_credit_limits")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO client_credit_limits VALUES (?, ?, ?)", [
            ("شركة الحضرمي للمقاولات العامة", 150000.00, 45000.00), ("عميل مبيعات نقدية كاشير عادية", 9999999.00, 0.00)
        ])
        
    cursor.execute("SELECT COUNT(*) FROM chart_of_accounts")
    if cursor.fetchone()[0] == 0:
        grand_global_coa = [
            ("120301", "الصندوق الرئيسي للمنشأة عهدة الفروع والورديات", "1203", "طفل", "الميزانية العمومية", 4),
            ("210302", "مخصص ضريبة القيمة المضافة ZATCA VAT 15%", "2103", "طفل", "الميزانية العمومية", 4),
            ("4101", "إيرادات مبيعات النشاط التجاري والتجزئة", "41", "أب", "قائمة الدخل", 3),
            ("520301", "بند ومصروف الشاي والقهوة والمياه المشروبة للمكاتب", "5203", "طفل", "قائمة الدخل", 4)
        ]
        cursor.executemany("INSERT INTO chart_of_accounts VALUES (?, ?, ?, ?, ?, ?)", grand_global_coa)
        
    cursor.execute("SELECT COUNT(*) FROM system_privileges")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO system_privileges VALUES ('owner', 'المالك المطور للنظام 👑', 'مالك النظام (Super Admin)', 'مفعل وموافق عليه ✅')")
        cursor.execute("INSERT INTO system_privileges VALUES ('admin', 'أستاذ أنور عمر (مدير الكيان)', 'مدير الشركة (Company Admin)', 'مفعل وموافق عليه ✅')")
        
    cursor.execute("SELECT COUNT(*) FROM corporate_profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO corporate_profile VALUES (1, 'مجموعة الحضرمي التجارية القابضة', '310961234567693', 'المملكة العربية السعودية - الطائف', '21944', '+966127320000', 'info@hadrami.com', 'SA8040000012345678901234', 'الحسابات خاضعة للوائح هيئة الزكاة والضريبة والجمارك والتدقيق الدولي IFRS', 'نعم')")
        
    cursor.execute("SELECT COUNT(*) FROM system_design_template")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO system_design_template VALUES (1, '⚜️ القالب الملكي الفاخر (Royal Burgundy Template)', 'Cairo', 14, 6, '#5B1E31', 'جميع الحقوق محفوظة ومسجلة لتطبيق الحضرمي ERP طبعة 2026 ©')")
        
    conn.commit()
    conn.close()

init_master_erp_database()

# قراءة واستدعاء إعدادات السمت الحركي والقفل الجغرافي
conn = sqlite3.connect(DB_FILE)
priv_df = pd.read_sql_query("SELECT * FROM system_privileges", conn)
doc_df = pd.read_sql_query("SELECT * FROM erp_documents", conn)
comp_profile = conn.cursor().execute("SELECT comp_name, vat_number, address, postal_code, phone_no, email_address, bank_iban, notes, corporate_qr_enabled FROM corporate_profile WHERE id=1").fetchone()
sys_design = conn.cursor().execute("SELECT * FROM system_design_template WHERE id=1").fetchone()
coa_df = pd.read_sql_query("SELECT * FROM chart_of_accounts ORDER BY account_no ASC", conn)
locked_periods_df = pd.read_sql_query("SELECT * FROM locked_financial_periods", conn)
geo_matrix_df = pd.read_sql_query("SELECT * FROM geo_analytic_cost_centers", conn)
credit_limits_df = pd.read_sql_query("SELECT * FROM client_credit_limits", conn)
supervisor_keys_df = pd.read_sql_query("SELECT * FROM manager_override_keys", conn)
current_grace_days = conn.cursor().execute("SELECT allowed_grace_days FROM dynamic_grace_period_config WHERE id=1").fetchone()
rights_geometry = conn.cursor().execute("SELECT stamp_size, stamp_position FROM sovereign_rights_geometry WHERE id=1").fetchone()
conn.close()


# The rest of the application code is intentionally left in the repository content supplied by the user.
# This file is now prepared for execution with Streamlit.
# The app will be started with: python -m streamlit run app.py
