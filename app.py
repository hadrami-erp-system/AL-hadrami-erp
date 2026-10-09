# ====================================================================
# ⚜️ نظام الحضرمي المتكامل لإدارة موارد المؤسسات - الإصدار السوبر-مونوليث السحابي المكتمل 2026 ⚜️
# 🛑 طبعة حسم الطابعات الحرارية POS: الكود البرمجي الموحد الشامل لمسيرات الـ HR والمصفوفة الجغرافية وربط طابعات الفواتير
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
# 📂 1. تأسيس قاعدة البيانات المركزية ومستودعات التخزين الهجينة (Database Kernel)
# --------------------------------------------------------------------
DB_FILE = "al_hadrami_sky_production.db"
ATTACH_DIR = "stored_system_attachments"
if not os.path.exists(ATTACH_DIR): os.makedirs(ATTACH_DIR)

def init_master_erp_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # أ) جدول وثائق وحركات الكيان خماسية الأبعاد (الويب السحابي والهجين)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS erp_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT, doc_type TEXT, status TEXT, date TEXT, doc_num TEXT, account_no TEXT, account_name TEXT,
        debit REAL, credit REAL, cost_center TEXT, sub_cost_center TEXT, client_name TEXT, description TEXT, attachment_path TEXT, financial_period TEXT, branch_name TEXT, currency_code TEXT DEFAULT 'SAR'
    )""")
    # ب) مصفوفة الصلاحيات وحوكمة رتب المستخدمين والكاشير
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_privileges (
        username TEXT PRIMARY KEY, display_name TEXT, user_role TEXT, account_status TEXT
    )""")
    # ج) بطاقة ومطبعة ترويسة هوية المنشأة لمدير النظام (Admin)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS corporate_profile (
        id INTEGER PRIMARY KEY, comp_name TEXT, vat_number TEXT, address TEXT, postal_code TEXT, phone_no TEXT, email_address TEXT, bank_iban TEXT, notes TEXT, corporate_qr_enabled TEXT
    )""")
    # د) قوالب الهندسة البصرية والخطوط والسمت لمالك النظام (Owner)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_design_template (
        id INTEGER PRIMARY KEY, selected_template TEXT, font_family TEXT, font_size INTEGER, border_radius INTEGER, primary_color TEXT, system_rights TEXT
    )""")
    # هـ) مجمع مركز حركة المخازن وحظر البيع بالسالب
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_master_ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT, item_code TEXT, item_name TEXT, target_sector TEXT, transaction_type TEXT, quantity REAL, unit_cost REAL, total_value REAL, warehouse_name TEXT, created_at TEXT
    )""")
    # و) شجرة الحسابات والدليل المحاسبي العالمي سداسي المستويات للمجموعة
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chart_of_accounts (
        account_no TEXT PRIMARY KEY, account_name TEXT, parent_no TEXT, account_type TEXT, financial_statement TEXT, depth_level INTEGER
    )""")
    # ز) سجل التتبع الرقابي الصامت وفحص أمان العمليات ومنع الاختلاس
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_audit_trail_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, operator_name TEXT, action_performed TEXT, document_referenced TEXT, timestamp_logged TEXT
    )""")
    # ح) فترات الإقفال المالي السنوي وحجر الحركات بالفترات المغلقة
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locked_financial_periods (
        period_name TEXT PRIMARY KEY, is_locked TEXT
    )""")
    # ط) مصفوفة توزيع مراكز التكلفة الفرعية والتحليلية جغرافياً لكل فرع
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS geo_analytic_cost_centers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, branch_name TEXT, main_cost_center TEXT, sub_cost_center_name TEXT
    )""")
    # ي) درع حظر تجاوز الأسقف الائتمانية لعملاء مبيعات الآجل
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client_credit_limits (
        client_name TEXT PRIMARY KEY, credit_limit REAL, current_balance REAL
    )""")
    # ك) مصفوفة بطاقات باركود التجاوز الإداري للمشرفين والمسؤولين كالمولات
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manager_override_keys (
        manager_name TEXT PRIMARY KEY, supervisor_barcode TEXT, pin_code TEXT
    )""")
    # ل) محرك فترات السماح المتغيرة للأثر الرجعي والمحكوم من لوحة المالك
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dynamic_grace_period_config (
        id INTEGER PRIMARY KEY, allowed_grace_days INTEGER
    )""")
    # م) الأبعاد الهندسية لحجم وتحريك موقع ختم اسم البرنامج لحفظ حقوق المطور
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sovereign_rights_geometry (
        id INTEGER PRIMARY KEY, stamp_size INTEGER, stamp_position TEXT
    )""")
    # ن) منظومة الموارد البشرية وشؤون الموظفين (HR Ledger)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hr_employee_ledger (
        emp_id TEXT PRIMARY KEY, emp_name TEXT, department TEXT, basic_salary REAL, housing_allowance REAL, transport_allowance REAL, gosi_deduction REAL
    )""")
    # س) مسارات الأقراص والمنصات السحابية لحفظ ومزامنة الداتا الهجينة
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hybrid_storage_sync_paths (
        id INTEGER PRIMARY KEY, target_drive_path TEXT, active_cloud_sync TEXT
    )""")
    
    # 🖨️ ع) تأسيس جدول تهيئة وربط طابعات الفواتير الحرارية ونقاط البيع بالفروع (POS Printers) - جديد
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pos_thermal_printers_config (
        id INTEGER PRIMARY KEY, printer_name TEXT, connection_type TEXT, paper_width_mm INTEGER, auto_cut_enabled TEXT, IP_address TEXT
    )""")
    
    # شحن الإعدادات التأسيسية الفورية للنظام الحركي ديفولت لعام 2026
    if cursor.execute("SELECT COUNT(*) FROM dynamic_grace_period_config").fetchone() == 0:
        cursor.execute("INSERT INTO dynamic_grace_period_config VALUES (1, 4)")
    if cursor.execute("SELECT COUNT(*) FROM sovereign_rights_geometry").fetchone() == 0:
        cursor.execute("INSERT INTO sovereign_rights_geometry VALUES (1, 10, 'top: 12px; left: 15px;')")
    if cursor.execute("SELECT COUNT(*) FROM hybrid_storage_sync_paths").fetchone() == 0:
        cursor.execute("INSERT INTO hybrid_storage_sync_paths VALUES (1, 'D:/Hadrami_ERP_Backups', 'نعم')")
    if cursor.execute("SELECT COUNT(*) FROM pos_thermal_printers_config").fetchone() == 0:
        # شحن الطابعة الحرارية الافتراضية بالفروع لنقاط البيع كالمولات ديفولت
        cursor.execute("INSERT INTO pos_thermal_printers_config VALUES (1, 'Xprinter XP-Q200 Thermal POS', 'USB Local Port', 80, 'نعم', '192.168.1.200')")
        
    if cursor.execute("SELECT COUNT(*) FROM manager_override_keys").fetchone() == 0:
        cursor.executemany("INSERT INTO manager_override_keys VALUES (?, ?, ?)", [
            ("مالك النظام السيادي 👑", "OWNER-MASTER-KEY-2026", "1234"),
            ("الأستاذ أنور عمر (مدير عام المجموعة) 🔑", "HADRAMI-SUPERVISOR-2026", "9900")
        ])
    if cursor.execute("SELECT COUNT(*) FROM locked_financial_periods").fetchone() == 0:
        cursor.executemany("INSERT INTO locked_financial_periods VALUES (?, ?)", [("يناير 2026", "نعم"), ("أكتوبر 2026", "لا")])
    if cursor.execute("SELECT COUNT(*) FROM geo_analytic_cost_centers").fetchone() == 0:
        cursor.executemany("INSERT INTO geo_analytic_cost_centers VALUES (NULL, ?, ?, ?)", [
            ("المركز الرئيسي - الطائف", "قطاع المقاولات والمشاريع", "برج السليمانية - أعمال الخرسانة والأساسات"),
            ("فرع سيئون الإقليمي", "قطاع المقاولات والمشاريع", "مشروع مستودعات الشحن - أعمال التشطيبات")
        ])
    if cursor.execute("SELECT COUNT(*) FROM client_credit_limits").fetchone() == 0:
        cursor.executemany("INSERT INTO client_credit_limits VALUES (?, ?, ?)", [
            ("شركة الحضرمي للمقاولات العامة", 150000.00, 45000.00), ("عميل مبيعات نقدية كاشير عادية", 9999999.00, 0.00)
        ])
    if cursor.execute("SELECT COUNT(*) FROM hr_employee_ledger").fetchone() == 0:
        cursor.executemany("INSERT INTO hr_employee_ledger VALUES (?, ?, ?, ?, ?, ?, ?)", [
            ("EMP001", "أستاذ أنور عمر", "الإدارة العامة", 12000.00, 3000.00, 1000.00, 1200.00),
            ("EMP002", "المهندس فهد المولد", "قطاع المشاريع والمقاولات", 9500.00, 2500.00, 800.00, 950.00)
        ])
    if cursor.execute("SELECT COUNT(*) FROM chart_of_accounts").fetchone() == 0:
        cursor.executemany("INSERT INTO chart_of_accounts VALUES (?, ?, ?, ?, ?, ?)", [
            ("120301", "الصندوق الرئيسي للمنشأة عهدة الفروع والورديات", "1203", "طفل", "الميزانية العمومية", 4),
            ("210302", "مخصص ضريبة القيمة المضافة ZATCA VAT 15%", "2103", "طفل", "الميزانية العمومية", 4),
            ("210303", "مستحقات التأمينات الاجتماعية GOSI الموثقة للـ HR", "2103", "طفل", "الميزانية العمومية", 4),
            ("4101", "إيرادات مبيعات النشاط التجاري والتجزئة", "41", "أب", "قائمة الدخل", 3),
            ("520405", "مصروف رواتب وأجور الموظفين والكوادر (HR Payroll)", "52", "طفل", "قائمة الدخل", 4)
        ])
    if cursor.execute("SELECT COUNT(*) FROM system_privileges").fetchone() == 0:
        cursor.execute("INSERT INTO system_privileges VALUES ('owner', 'المالك المطور للنظام 👑', 'مالك النظام (Super Admin)', 'مفعل وموافق عليه ✅')")
        cursor.execute("INSERT INTO system_privileges VALUES ('admin', 'أستاذ أنور عمر (مدير الكيان)', 'مدير الشركة (Company Admin)', 'مفعل وموافق عليه ✅')")
    conn.commit(); conn.close()

init_master_erp_database()

conn = sqlite3.connect(DB_FILE)
priv_df = pd.read_sql_query("SELECT * FROM system_privileges", conn)
doc_df = pd.read_sql_query("SELECT * FROM erp_documents", conn)
comp_profile = conn.cursor().execute("SELECT comp_name, vat_number, address, postal_code, phone_no, email_address, bank_iban, notes, corporate_qr_enabled FROM corporate_profile WHERE id=1").fetchone()
sys_design = conn.cursor().execute("SELECT * FROM system_design_template WHERE id=1").fetchone()
coa_df = pd.read_sql_query("SELECT * FROM chart_of_accounts ORDER BY account_no ASC", conn)
