import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة لتكون عريضة وفخمة ومناسبة لنظام المربعات
st.set_page_config(page_title="منظومة إدارة المجاميع التعليمية", page_icon="📚", layout="wide")

# تصميم ستايل مخصص (CSS) مدمج: مظهر داكن + بطاقات مربعة أنيقة تشبه أنظمة الفنادق والغرف
st.markdown("""
    <style>
    /* المظهر العام الداكن للموقع */
    .main { 
        background-color: #1a1a1a; 
        color: #ffffff; 
    }
    
    /* تصميم البطاقة المربعة للجروب */
    .group-box {
        background-color: #222831;
        border: 2px solid #00adb5;
        border-radius: 15px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        margin-bottom: 25px;
        color: #ffffff;
        transition: transform 0.3s, border-color 0.3s;
    }
    
    /* حركة تفاعلية عند مرور الماوس فوق المربع */
    .group-box:hover {
        transform: translateY(-5px);
        border-color: #00f3ff;
    }
    
    /* عنوان الجروب داخل المربع */
    .group-name {
        font-size: 28px;
        font-weight: bold;
        color: #00adb5;
        margin-bottom: 15px;
    }
    
    /* الإحصائيات داخل المربع */
    .group-count {
        font-size: 18px;
        color: #eeeeee;
        background-color: #393e46;
        padding: 8px 15px;
        border-radius: 8px;
        display: inline-block;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ملف حفظ البيانات محلياً لمنع ضياع أسماء الطلاب
DATA_FILE = "students_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["اسم الطالب", "المجموعة / الكروب", "رقم الهاتف", "رقم ولي الأمر"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# المجاميع الافتراضية في النظام
if "available_groups" not in st.session_state:
    st.session_state.available_groups = ["(بنين) A كروب", "(بنات) B كروب"]

# قراءة أي كروب إضافي تم حفظه سابقاً في ملف الـ CSV
for g in df["المجموعة / الكروب"].dropna().unique():
    if g not in st.session_state.available_groups:
        st.session_state.available_groups.append(g)

# --- الواجهة الرئيسية ---
st.markdown("<h1 style='color: #00adb5; text-align: center; font-family: Cairo, sans-serif;'>إدارة مجاميع الخصوصي المطورة 📚</h1>", unsafe_allow_html=True)
st.write("---")

# لوحة التحكم الجانبية لإضافة كروب جديد في أي وقت
with st.sidebar:
    st.markdown("<h2 style='color: #00adb5;'>⚙️ التحكم بالنظام</h2>", unsafe_allow_html=True)
    st.subheader("➕ إضافة كروب جديد")
    new_group = st.text_input("اكتب اسم الكروب الجديد:")
    if st.button("حفظ الكروب في القائمة"):
        if new_group and new_group not in st.session_state.available_groups:
            st.session_state.available_groups.append(new_group)
            st.success(f"✅ تم إضافة: {new_group}")
            st.rerun()

# قسم استمارة تسجيل الطلاب الجدد
st.subheader("📝 تسجيل طالب جديد")
with st.expander("اضغط هنا لفتح استمارة التسجيل وتعبئة البيانات"):
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("اسم الطالب الثلاثي")
        student_group = st.selectbox("اختر المجموعة / الكروب", st.session_state.available_groups)
    with col2:
        student_phone = st.text_input("رقم هاتف الطالب")
        parent_phone = st.text_input("رقم هاتف ولي الأمر")
    
    if st.button("💾 حفظ الطالب في النظام"):
        if student_name and student_phone:
            new_student = pd.DataFrame([[student_name, student_group, student_phone, parent_phone]], 
                                       columns=["اسم الطالب", "المجموعة / الكروب", "رقم الهاتف", "رقم ولي الأمر"])
            df = pd.concat([df, new_student], ignore_index=True)
            save_data(df)
            st.success(f"🎉 تم تسجيل الطالب {student_name} بنجاح!")
            st.rerun()
        else:
            st.error("الرجاء كتابة اسم الطالب ورقم هاتفه!")

st.write("---")

# --- عرض الكروبات بنظام المربعات (مثل واجهة الفندق!) ---
st.subheader("🗂️ لوحة المجاميع الحالية (نظام البطاقات المشنفة)")

# تقسيم العرض برمجياً إلى 3 أعمدة لتظهر المربعات بجانب بعضها بشكل متناسق
cols = st.columns(3)

for index, group in enumerate(st.session_state.available_groups):
    # حساب عدد الطلاب الفعليين داخل هذا الكروب بالتحديد
    count_students = len(df[df["المجموعة / الكروب"] == group])
    
    # توزيع الكروبات على الأعمدة الثلاثة بالتناوب
    with cols[index % 3]:
        # رسم المربع بتنسيق HTML و CSS المطورين في الأعلى
        st.markdown(f"""
            <div class="group-box">
                <div class="group-name">📁 {group}</div>
                <div class="group-count">👥 الطلاب: <b>{count_students}</b></div>
            </div>
        """, unsafe_allow_html=True)
        
        # صندوق منبثق أنيق يفتح تحت المربع مباشرة لإدارة وحذف طلاب هذا الكروب
        with st.popover(f"🔍 استعراض وإدارة طلاب {group}"):
            group_df = df[df["المجموعة / الكروب"] == group]
            if not group_df.empty:
                for idx, row in group_df.iterrows():
                    col_s1, col_s2 = st.columns([4, 1])
                    with col_s1:
                        st.write(f"👤 **{row['اسم الطالب']}**\n📞 {row['رقم الهاتف']}")
                    with col_s2:
                        # زر الحذف السريع للطالب بوضع علامة ضرب إكس
                        if st.button("❌", key=f"del_{idx}"):
                            df = df.drop(idx)
                            save_data(df)
                            st.success("تم الحذف!")
                            st.rerun()
                    st.write("---")
            else:
                st.write("لا يوجد طلاب مسجلين في هذه المجموعة حالياً.")

st.write("---")

# قاعدة البيانات الكلية والبحث المباشر عن أي اسم
st.subheader("🔍 قاعدة بيانات الطلاب والبحث السريع")
search_query = st.text_input("ادخل اسم الطالب للبحث الفوري عنه:")

if not df.empty:
    if search_query:
        filtered_df = df[df["اسم الطالب"].str.contains(search_query, case=False, na=False)]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
else:
    st.info("💡 النظام فارغ حالياً. بمجرد تسجيل الطلاب ستظهر البيانات هنا.")
