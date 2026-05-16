import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة لتكون عصرية وواسعة تشبه أنظمة الفنادق
st.set_page_config(page_title="منظومة إدارة المجاميع التعليمية", page_icon="📚", layout="wide")

# تطبيق تصميم داكن وفخم عبر الـ CSS
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    h1 { color: #00adb5; text-align: center; font-family: 'Cairo', sans-serif; }
    .stButton>button { background-color: #00adb5; color: white; border-radius: 8px; width: 100%; font-size: 16px; }
    .stButton>button:hover { background-color: #007a80; color: white; }
    div[data-testid="stDataFrame"] { background-color: #222831; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# اسم ملف حفظ البيانات محلياً على الحاسوب دون إنترنت
DATA_FILE = "students_data.csv"

# دالة تحميل البيانات
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["اسم الطالب", "المجموعة / الكروب", "رقم الهاتف", "رقم ولي الأمر"])

# دالة حفظ البيانات
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# تحميل البيانات الحالية
df_students = load_data()

# عنوان البرنامج الرئيسي
st.markdown("<h1>📚 منظومة إدارة مجاميع الخصوصي المطورة</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #eeeeee;'>نظام محلي ذكي لإدارة بيانات الطلاب والكروبات بسلاسة</p>", unsafe_allow_html=True)
st.write("---")

# تقسيم الشاشة إلى عمودين (مثل أنظمة الفنادق: لوحة تحكم جانبية + جدول عرض)
col1, col2 = st.columns([1, 2], gap="large")

# العمود الأول: لوحة إضافة الطلاب
with col1:
    st.markdown("<h3 style='color: #00adb5;'>➕ تسجيل طالب جديد</h3>", unsafe_allow_html=True)
    with st.form("student_form", clear_on_submit=True):
        student_name = st.text_input("اسم الطالب الثلاثي:")
        group_name = st.selectbox("اختر المجموعة / الكروب:", ["كروب A (بنين)", "كروب B (بنات)", "كروب C", "كروب D"])
        phone_number = st.text_input("رقم هاتف الطالب:")
        parent_phone = st.text_input("رقم هاتف ولي الأمر:")
        
        submit_btn = st.form_submit_button("حفظ الطالب في النظام")
        
        if submit_btn:
            if student_name.strip() != "":
                new_student = pd.DataFrame([[student_name, group_name, phone_number, parent_phone]], 
                                            columns=["اسم الطالب", "المجموعة / الكروب", "رقم الهاتف", "رقم ولي الأمر"])
                df_students = pd.concat([df_students, new_student], ignore_index=True)
                save_data(df_students)
                st.success(f"✔️ تم تسجيل الطالب ({student_name}) بنجاح!")
                st.rerun()
            else:
                st.error("⚠️ يرجى كتابة اسم الطالب أولاً!")

# العمود الثاني: عرض البيانات والبحث والفلترة
with col2:
    st.markdown("<h3 style='color: #00adb5;'>🔍 قاعدة بيانات الطلاب والبحث</h3>", unsafe_allow_html=True)
    
    # خانة البحث الفوري
    search_query = st.text_input("اكتب اسم الطالب للبحث عنه فوراً:")
    
    # قائمة الفلترة حسب الكروب
    filter_group = st.selectbox("تصفية وعرض حسب الكروب:", ["عرض الكل", "كروب A (بنين)", "كروب B (بنات)", "كروب C", "كروب D"])
    
    # تطبيق التصفية والبحث على الجدول
    filtered_df = df_students.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df["اسم الطالب"].str.contains(search_query, na=False, case=False)]
    if filter_group != "عرض الكل":
        filtered_df = filtered_df[filtered_df["المجموعة / الكروب"] == filter_group]
    
    # عرض الجدول الاحترافي للبيانات
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        st.info(f"📊 عدد الطلاب المعروضين حالياً: {len(filtered_df)} طالب")
    else:
        st.warning("📂 لا توجد بيانات طلاب مطابقة للبحث حالياً.")

    # خيار حذف طالب لتنظيف القائمة
    st.write("---")
    st.markdown("<h4 style='color: #ff4b4b;'>🗑️ إدارة وحذف الطلاب</h4>", unsafe_allow_html=True)
    if not df_students.empty:
        student_to_delete = st.selectbox("اختر اسم الطالب المراد حذفه نهائياً:", [""] + df_students["اسم الطالب"].tolist())
        if st.button("حذف الطالب المحدد"):
            if student_to_delete:
                df_students = df_students[df_students["اسم الطالب"] != student_to_delete]
                save_data(df_students)
                st.success(f"❌ تم حذف الطالب ({student_to_delete}) من المنظومة.")
                st.rerun()
            else:
                st.warning("⚠️ الرجاء اختيار اسم طالب لحذفه.")