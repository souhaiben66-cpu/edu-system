import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="منظومة إدارة الطلاب", page_icon="🎓", layout="wide")

# تطبيق المظهر الداكن المخصص والستاينق
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    .group-box {
        background-color: #222831;
        border: 2px solid #00adb5;
        border-radius: 15px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        margin-bottom: 25px;
        color: #ffffff;
    }
    .student-card {
        background-color: #2d3748;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00adb5;
        margin-bottom: 20px;
    }
    .receipt-box {
        background-color: #fff;
        color: #000;
        padding: 20px;
        border-radius: 8px;
        border: 2px dashed #000;
        font-family: 'Courier New', Courier, monospace;
    }
    /* ستايل خاص بالطباعة */
    @media print {
        body * { visibility: hidden; }
        .receipt-box, .receipt-box * { visibility: visible; }
        .receipt-box { position: absolute; left: 0; top: 0; width: 100%; }
    }
    </style>
""", unsafe_allow_html=True)

# 1. إنشاء ذاكرة تخزين مؤقتة للبيانات (إذا لم تكن موجودة)
if "students" not in st.session_state:
    # بيانات تجريبية مبدئية
    st.session_state.students = [
        {"id": 1, "name": "أحمد علي", "phone": "7709971745", "group": "(بنين) A كروب", "address": "الموصل - الزهور", "total_fee": 1000, "paid_fee": 400},
        {"id": 2, "name": "محمد جاسم", "phone": "5413524151", "group": "(بنين) A كروب", "address": "الموصل - المهندسين", "total_fee": 1200, "paid_fee": 600}
    ]

st.title("🎓 منظومة إدارة شؤون الطلاب والأقساط")

# 2. حساب عدد الطلاب في الكروبات (العدادات فوق)
group_A_count = sum(1 for s in st.session_state.students if s['group'] == "(بنين) A كروب")
group_B_count = sum(1 for s in st.session_state.students if s['group'] == "كروب B (بنات)")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="group-box"><h3>(بنين) A كروب 📂</h3><p>الطلاب: {group_A_count} 👥</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="group-box"><h3>كروب B (بنات) 📂</h3><p>الطلاب: {group_B_count} 👥</p></div>', unsafe_allow_html=True)

# 3. قسم إضافة طالب جديد (مع ميزة السكن والأقساط الجديدة)
with st.expander("➕ إضافة طالب جديد للمنظومة"):
    with st.form("add_student_form", clear_on_submit=True):
        new_name = st.text_input("اسم الطالب الثلاثي:")
        new_phone = st.text_input("رقم الهاتف:")
        new_group = st.selectbox("المجموعة / الكروب:", ["(بنين) A كروب", "كروب B (بنات)"])
        new_address = st.text_input("سكن الطالب (العنوان):")
        new_total = st.number_input("إجمالي قسط الدراسة (دنانير/دولار):", min_value=0, value=1000, step=50)
        new_paid = st.number_input("المبلغ المدفوع حالياً:", min_value=0, value=0, step=50)
        
        submit_btn = st.form_submit_button("حفظ الطالب")
        if submit_btn and new_name and new_phone:
            new_id = max([s['id'] for s in st.session_state.students]) + 1 if st.session_state.students else 1
            st.session_state.students.append({
                "id": new_id, "name": new_name, "phone": new_phone, 
                "group": new_group, "address": new_address, 
                "total_fee": new_total, "paid_fee": new_paid
            })
            st.success(f"تم إضافة الطالب {new_name} بنجاح!")
            st.rerun()

# 4. عرض جدول الطلاب العام
st.subheader("📋 قائمة الطلاب المسجلين")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    # تصفية الأعمدة للعرض فقط
    df_display = df[["name", "phone", "group", "address"]].rename(columns={
        "name": "اسم الطالب", "phone": "رقم الهاتف", "group": "المجموعة / الكروب", "address": "السكن"
    })
    st.dataframe(df_display, use_container_width=True)
else:
    st.info("لا يوجد طلاب مسجلين حالياً.")

# 5. قسم إدارة واختيار طالب (لعرض معلوماته، تعديله، حذفه، وطباعة وصله)
st.subheader("🔍 استعراض وتعديل وإدارة طالب معين")
student_names = [s['name'] for s in st.session_state.students]

if student_names:
    selected_student_name = st.selectbox("اختر اسم الطالب لإدارة ملفه المالي والشخصي:", student_names)
    # جلب بيانات الطالب المختار
    student_idx = next(i for i, s in enumerate(st.session_state.students) if s['name'] == selected_student_name)
    student = st.session_state.students[student_idx]
    
    # حساب القسط المتبقي تلقائياً
    remaining_fee = student['total_fee'] - student['paid_fee']
    
    # عرض معلومات الطالب داخل بطاقة ملونة ومجسمة
    st.markdown(f"""
    <div class="student-card">
        <h4>📋 المعلومات الشخصية والمالية للطالب: {student['name']}</h4>
        <p><b>📍 السكن:</b> {student['address']} | <b>📞 الهاتف:</b> {student['phone']} | <b>🗂️ الكروب:</b> {student['group']}</p>
        <hr>
        <h5 style='color: #00adb5;'>💰 الموقف المالي:</h5>
        <p>💵 <b>إجمالي القسط الكلّي:</b> {student['total_fee']}</p>
        <p>🟢 <b style='color: #4caf50;'>القسط المدفوع (الواصل):</b> {student['paid_fee']}</p>
        <p>🔴 <b style='color: #f44336;'>القسط المتبقي (المطلوب):</b> {remaining_fee}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # أزرار الإجراءات (تحديث قسط، تعديل بيانات، حذف، طباعة)
    tab1, tab2, tab3 = st.tabs(["💵 تحديث وطباعة القسط", "✏️ تعديل البيانات الشخصية", "❌ حذف الطالب"])
    
    with tab1:
        st.write("### 🧾 دفع قسط جديد وطباعة الوصل")
        pay_amount = st.number_input("أدخل المبلغ الذي سدده الطالب الآن:", min_
