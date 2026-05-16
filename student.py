import streamlit as st

# إعدادات الصفحة الأساسية لتكون مريحة وعريضة
st.set_page_config(page_title="منظومة إدارة المجاميع والطلاب", layout="wide", initial_sidebar_state="expanded")

# تصميم ستايل مخصص (CSS) لجعل البطاقات تشبه صورتك تماماً
st.markdown("""
    <style>
    .group-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .group-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .group-title {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .group-stat {
        font-size: 16px;
        color: #7f8c8d;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_allowed_html=True)

# إدارة البيانات باستخدام الذاكرة المؤقتة (Session State)
if 'groups' not in st.session_state:
    st.session_state.groups = ["(بنين) A كروب", "(بنات) B كروب"]

if 'students' not in st.session_state:
    st.session_state.students = []

# --- القائمة الجانبية (Sidebar) لإضافة كروب جديد ---
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    st.subheader("➕ إضافة كروب جديد")
    new_group_name = st.text_input("اكتب اسم الكروب الجديد:")
    if st.button("حفظ الكروب المطور"):
        if new_group_name and new_group_name not in st.session_state.groups:
            st.session_state.groups.append(new_group_name)
            st.success(f"✅ تم إضافة {new_group_name}")
            st.rerun()
        else:
            st.error("الاسم فارغ أو موجود مسبقاً!")

# --- الواجهة الرئيسية للموقع ---
st.title("📚 لوحة إدارة مجاميع الخصوصي المطورة")
st.write("---")

# 1. قسم تسجيل الطلاب الجدد
st.subheader("📝 تسجيل طالب جديد في النظام")
with st.expander("اضغط هنا لفتح استمارة التسجيل الإلكترونية"):
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("اسم الطالب الثلاثي:")
        selected_group = st.selectbox("اختر المجموعة / الكروب:", st.session_state.groups)
    with col2:
        student_phone = st.text_input("رقم هاتف الطالب:")
        parent_phone = st.text_input("رقم هاتف ولي الأمر:")
    
    if st.button("💾 حفظ الطالب في النظام"):
        if student_name and student_phone:
            st.session_state.students.append({
                "name": student_name,
                "group": selected_group,
                "phone": student_phone,
                "parent": parent_phone
            })
            st.success(f"🎉 تم تسجيل الطالب {student_name} بنجاح!")
            st.rerun()
        else:
            st.error("الرجاء ملء اسم الطالب ورقم الهاتف على الأقل!")

st.write("---")

# 2. عرض الكروبات على شكل بطاقات مربعة (مثل نظام الغرف بالفندق!)
st.subheader("🗂️ عرض المجاميع الحالية (نظام البطاقات)")

# نقسم الصفحة إلى 3 أعمدة لعرض البطاقات بجانب بعضها
cols = st.columns(3)
for index, group in enumerate(st.session_state.groups):
    # حساب عدد الطلاب داخل هذا الكروب حالياً
    count_students = sum(1 for s in st.session_state.students if s['group'] == group)
    
    with cols[index % 3]:
        # كود الـ HTML لصنع البطاقة المربعة الأنيقة
        st.markdown(f"""
            <div class="group-card">
                <div class="group-title">👤 {group}</div>
                <div class="group-stat">📋 إجمالي الطلاب: <b>{count_students}</b></div>
                <div class="group-stat">⏰ المحاضرة القادمة: السبت 4:00 م</div>
            </div>
        """, unsafe_allow_html=True)
        
        # زر لعرض طلاب هذا الكروب بالتحديد تحت البطاقة
        with st.popover(f"🔍 استعراض طلاب {group}"):
            group_students = [s for s in st.session_state.students if s['group'] == group]
            if group_students:
                for s in group_students:
                    st.write(f"• **{s['name']}** - هاتف: {s['phone']}")
            else:
                st.write("لا يوجد طلاب مسجلين في هذا الكروب حالياً.")

st.write("---")

# 3. قاعدة البيانات الإجمالية والبحث
st.subheader("🔍 قاعدة بيانات الطلاب العامة والبحث المباشر")
search_query = st.text_input("🕵️ اكتب اسم الطالب للبحث عنه فوراً:")

if st.session_state.students:
    filtered_students = [s for s in st.session_state.students if search_query.lower() in s['name'].lower()]
    if filtered_students:
        st.table(filtered_students)
    else:
        st.warning("لا توجد بيانات مطابقة للبحث حالياً.")
else:
    st.info("💡 النظام فارغ، قم بتسجيل أول طالب لتظهر البيانات هنا.")
