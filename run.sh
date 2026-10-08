#!/bin/bash
# 🚀 سكريبت التشغيل

echo "⚜️ نظام الحضرمي ERP 2026"
echo "================================"
echo ""
echo "📦 تثبيت المكتبات..."
pip install -r requirements.txt

echo ""
echo "🚀 بدء التطبيق..."
echo ""
echo "📍 رابط التطبيق: http://localhost:8501"
echo ""

streamlit run app.py --server.port=8501 --server.address=0.0.0.0
