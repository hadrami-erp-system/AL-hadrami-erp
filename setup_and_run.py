#!/usr/bin/env python3
# ====================================================================
# ⚜️ نظام الحضرمي ERP 2026 - ملف التشغيل التلقائي الشامل
# تجهيز + تثبيت + تشغيل مباشر
# ====================================================================

import subprocess
import sys
import os
import platform

def print_header():
    """طباعة رأس النظام"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║          ⚜️  نظام الحضرمي ERP 2026  ⚜️                   ║
    ║     نظام إدارة موارد المؤسسات المتكامل                    ║
    ║              الطبعة السحابية 2026                        ║
    ║                                                            ║
    ║  🔧 في جاري التجهيز والتشغيل الآن...                    ║
    ╚════════════════════════════════════════════════════════════╝
    """)

def print_step(step_num, description):
    """طباعة خطوة التشغيل"""
    print(f"\n{'='*60}")
    print(f"📍 الخطوة {step_num}: {description}")
    print(f"{'='*60}")

def check_python_version():
    """التحقق من إصدار Python"""
    print_step(1, "التحقق من Python")
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ خطأ: يتطلب Python 3.8 أو أحدث")
        sys.exit(1)
    return True

def install_requirements():
    """تثبيت المكتبات المطلوبة"""
    print_step(2, "تثبيت المكتبات")
    requirements = [
        "streamlit>=1.35.0",
        "pandas>=2.0.0",
        "qrcode[pil]>=7.4.2",
        "Pillow>=10.0.0",
        "pyarrow>=14.0.0"
    ]
    
    for req in requirements:
        print(f"📦 جاري تثبيت: {req}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", req])
            print(f"   ✅ تم بنجاح")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  خطأ في التثبيت: {e}")
            return False
    
    return True

def setup_directories():
    """إعداد المجلدات المطلوبة"""
    print_step(3, "إعداد المجلدات")
    
    import tempfile
    
    directories = {
        "TEMP_DIR": tempfile.gettempdir(),
        "DB_PATH": os.path.join(tempfile.gettempdir(), "al_hadrami_sky_production.db"),
        "ATTACH_DIR": os.path.join(tempfile.gettempdir(), "attachments"),
        "BACKUP_DIR": os.path.join(tempfile.gettempdir(), "backups")
    }
    
    for name, path in directories.items():
        if "attachments" in path or "backups" in path:
            os.makedirs(path, exist_ok=True)
            print(f"✅ {name}: {path}")
        else:
            print(f"✅ {name}: {path}")
    
    return directories

def display_system_info():
    """عرض معلومات النظام"""
    print_step(4, "معلومات النظام")
    
    print(f"🖥️  نظام التشغيل: {platform.system()} {platform.release()}")
    print(f"🐍 إصدار Python: {platform.python_version()}")
    print(f"📍 المسار الحالي: {os.getcwd()}")
    
    return True

def initialize_database():
    """تهيئة قاعدة البيانات"""
    print_step(5, "تهيئة قاعدة البيانات")
    
    import sqlite3
    import tempfile
    
    DB_FILE = os.path.join(tempfile.gettempdir(), "al_hadrami_sky_production.db")
    
    try:
        conn = sqlite3.connect(DB_FILE)
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
        print("   ✅ جدول المستندات")
        
        # جدول الموظفين
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_privileges (
            username TEXT PRIMARY KEY,
            display_name TEXT,
            user_role TEXT,
            account_status TEXT
        )""")
        print("   ✅ جدول الموظفين والصلاحيات")
        
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
        print("   ✅ جدول بيانات الشركة")
        
        # جدول المخزون
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_master_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_code TEXT, item_name TEXT, quantity REAL,
            unit_cost REAL, total_value REAL, warehouse_name TEXT,
            created_at TEXT
        )""")
        print("   ✅ جدول المخزون")
        
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
        print("   ✅ جدول دليل الحسابات")
        
        # جدول الفترات المالية
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS locked_financial_periods (
            period_name TEXT PRIMARY KEY,
            is_locked TEXT
        )""")
        print("   ✅ جدول الفترات المالية")
        
        # جدول مراكز التكلفة
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS geo_analytic_cost_centers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_name TEXT,
            main_cost_center TEXT,
            sub_cost_center_name TEXT
        )""")
        print("   ✅ جدول مراكز التكلفة")
        
        # جدول حدود الائتمان
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS client_credit_limits (
            client_name TEXT PRIMARY KEY,
            credit_limit REAL,
            current_balance REAL
        )""")
        print("   ✅ جدول حدود الائتمان")
        
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
            conn.commit()
            print("   ✅ تم إضافة الموظفين الافتراضيين")
        
        cursor.execute("SELECT COUNT(*) FROM corporate_profile")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO corporate_profile VALUES 
            (1, 'مجموعة الحضرمي التجارية القابضة', '310961234567693',
            'الطائف - المملكة العربية السعودية', '21944', '+966127320000',
            'info@hadrami.com', 'SA8040000012345678901234',
            'الحسابات خاضعة للمعايير الدولية IFRS', 'نعم')
            """)
            conn.commit()
            print("   ✅ تم إضافة بيانات الشركة الافتراضية")
        
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
            conn.commit()
            print("   ✅ تم إضافة دليل الحسابات الافتراضي")
        
        cursor.execute("SELECT COUNT(*) FROM locked_financial_periods")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO locked_financial_periods VALUES (?, ?)",
                [("يناير 2026", "نعم"), ("فبراير 2026", "لا"), ("مارس 2026", "لا")]
            )
            conn.commit()
            print("   ✅ تم إضافة الفترات المالية")
        
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
            conn.commit()
            print("   ✅ تم إضافة مراكز التكلفة")
        
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
            print("   ✅ تم إضافة حدود الائتمان")
        
        conn.close()
        print(f"\n✅ قاعدة البيانات جاهزة: {DB_FILE}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تهيئة قاعدة البيانات: {e}")
        return False

def start_streamlit_app():
    """بدء تطبيق Streamlit"""
    print_step(6, "تشغيل التطبيق")
    
    print("\n🚀 جاري بدء نظام الحضرمي ERP...")
    print("\n📍 سيتم فتح التطبيق على: http://localhost:8501")
    print("\n⏳ جاري التحميل... (قد يستغرق بضع ثوان)")
    print("\n💡 نصيحة: إذا لم يفتح المتصفح تلقائياً، اضغط Ctrl+C واذهب لـ http://localhost:8501")
    print("\n" + "="*60)
    
    try:
        # التحقق من وجود app.py
        if not os.path.exists("app.py"):
            print("❌ خطأ: لم يتم العثور على app.py")
            print("تأكد من أنك في المجلد الصحيح")
            return False
        
        # تشغيل Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ])
        
        return True
    except KeyboardInterrupt:
        print("\n\n⛔ تم إيقاف التطبيق من قبل المستخدم")
        return False
    except Exception as e:
        print(f"❌ خطأ في تشغيل التطبيق: {e}")
        return False

def print_footer():
    """طباعة التذييل"""
    print("""
    
    ╔════════════════════════════════════════════════════════════╗
    ║                     ✅ تم التشغيل بنجاح                 ║
    ║                                                            ║
    ║  📧 البريد: info@hadrami.com                             ║
    ║  ☎️  الهاتف: +966127320000                               ║
    ║  📍 الموقع: الطائف، المملكة العربية السعودية             ║
    ║                                                            ║
    ║  © 2026 مجموعة الحضرمي التجارية القابضة                ║
    ║  جميع الحقوق محفوظة                                      ║
    ╚════════════════════════════════════════════════════════════╝
    """)

def main():
    """الدالة الرئيسية"""
    print_header()
    
    # التحقق من Python
    if not check_python_version():
        return
    
    # تثبيت المكتبات
    if not install_requirements():
        print("\n⚠️  تحذير: حدثت بعض المشاكل في التثبيت")
    
    # إعداد المجلدات
    directories = setup_directories()
    
    # عرض معلومات النظام
    display_system_info()
    
    # تهيئة قاعدة البيانات
    if not initialize_database():
        print("\n⚠️  تحذير: حدثت مشاكل في تهيئة قاعدة البيانات")
    
    # تشغيل التطبيق
    print_step(6, "تشغيل التطبيق")
    start_streamlit_app()
    
    print_footer()

if __name__ == "__main__":
    main()
