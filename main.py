import streamlit as st
import pandas as pd
from data_loader import load_assets
from report_generator import generate_styled_report
from validators import validate_search_criteria

st.set_page_config(page_title="نظام إدارة الأصول", layout="wide")
st.title("📊 نظام إدارة الأصول - الهيئة الجيولوجية السعودية")

uploaded_file = st.file_uploader("📂 حمّل ملف الأصول (Excel)", type=["xlsx"])

if uploaded_file:
    try:
        df = load_assets(uploaded_file)
        df.columns = df.columns.str.strip().str.replace(' ', '_')

        search_type = st.radio("اختر نوع التقرير", options=["general", "accounting"], format_func=lambda x: "عام" if x == "general" else "محاسبي")

        criteria = {}
        code = st.text_input("🔍 رمز الأصل")
        if code: criteria['Asset_Code_For_Accounting_Purpose'] = code

        city = st.text_input("🏙️ المدينة")
        if city: criteria['City'] = city

        gl_account = st.text_input("💼 الحساب العام")
        if gl_account: criteria['GL_account'] = gl_account

        min_cost, max_cost = st.slider("💰 مدى التكلفة", 0.0, 1_000_000.0, (0.0, 1_000_000.0), step=1000.0)
        criteria['Cost'] = [min_cost, max_cost]

        try:
            validate_search_criteria(criteria, df.columns)
            results = df.copy()
            for key, value in criteria.items():
                if isinstance(value, (list, tuple)):
                    results = results[results[key].between(*value)]
                else:
                    results = results[results[key] == value]

            columns = {
                'general': [
                    'Asset_Code_For_Accounting_Purpose',
                    'Asset_Description',
                    'City',
                    'Cost_Center',
                    'Quantity'
                ],
                'accounting': [
                    'Asset_Code_For_Accounting_Purpose',
                    'GL_account',
                    'Cost',
                    'Depreciation_amount',
                    'Useful_Life',
                    'Net_Book_Value'
                ]
            }
            results = results[columns[search_type]].dropna()

            st.success(f"تم العثور على {len(results)} أصل مطابق")
            st.dataframe(results.style.background_gradient(cmap='YlGnBu'))

        except Exception as e:
            st.error(f"⚠️ خطأ في معايير البحث: {str(e)}")

    except Exception as e:
        st.error(f"⚠️ حدث خطأ أثناء تحميل الملف: {str(e)}")
