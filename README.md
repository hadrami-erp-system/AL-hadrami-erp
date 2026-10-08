# 🚀 نظام الحضرمي ERP

## التشغيل المحلي
```bash
pip install -r requirements.txt
streamlit run app.py
```

## النشر السحابي
الأسهل: Streamlit Cloud
1. اذهب إلى https://share.streamlit.io/
2. اختر المستودع: `hadrami-erp-system/AL-hadrami-erp`
3. الفرع: `main`
4. الملف الرئيسي: `app.py`
5. اضغط Deploy

## Docker
```bash
docker build -t hadrami-erp .
docker run -p 8501:8501 hadrami-erp
```

## بيانات الدخول الافتراضية
- owner
- admin
- supervisor

يمكنك تعديل البيانات لاحقاً في قاعدة البيانات أو الكود.
