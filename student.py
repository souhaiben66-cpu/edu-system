import streamlit as st
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="منظومة إدارة الطلاب", page_icon="🎓", layout="wide")

# تصميم المظهر المخصص (CSS)
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; color: #ffffff; }
    
    /* تصميم الأزرار العلوية لتشبه الكروت الملونة */
    div.stButton > button {
        background-color: #222831 !important;
        border: 2px solid #00adb5 !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 20px 10px !important;
        width: 100% !important;
        min-height: 120px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        box-shadow: 0 8px 166px rgba(0,0,0,0.3) !important;
    }
    div.stButton > button:hover {
        border-color: #ffe600 !important;
    }
    
    .student-card {
        background-color: #2d3748;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00adb5;
        margin-bottom: 20px;
        color: white;
    }
    .receipt-box {
        background-color: #ffffff;
        color: #000000;
        padding: 25px;
        border-radius: 8px;
        border: 2px dashed #000000;
        font-family: 'Arial', sans-serif;
        margin-top: 15px;
    }
    .print-hint {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 1. قاعدة البيانات الثابتة - تم تعديل المجموعات لتطابق نصوصكِ السابقة بالضبط
if "students" not in st.session_state:
    st.session_state.students = [
        {"id": 1, "name": "أحمد علي", "phone": "7709971745", "group": "كروب A (بنين)", "address": "الموصل - الزهور", "total_fee": 1000, "paid_fee": 400},
        {"id": 2, "name": "محمد جاسم", "phone": "5413524151", "group": "كروب A (بنين)", "address": "الموصل - المهندسين", "total_fee": 1200, "paid_fee": 600},
        {"id": 3, "name": "عبد الله عمر", "phone": "7501234567", "group": "كروب A (بنين)", "address": "الموصل - المثنى", "total_fee": 1000, "paid_fee": 300},
        {"id": 4, "name": "فاطمة حسن", "phone": "7712233445", "group": "كروب B (بنات)", "address": "الموصل - الحدباء", "total_fee": 1000, "paid_fee": 1000}
    ]

# ذاكرة حفظ الفلتر الحالي
if "current_filter" not in st.session_state:
    st.session_state.current_filter = "الكل"

st.title("🎓 منظومة إدارة شؤون الطلاب والأقساط")

# 2. حساب عدد الطلاب الفعليين
count_A = sum(1 for s in st.session_state.students if s['group'] == "كروب A (بنين)")
count_B = sum(1 for s in st.session_state.students if s['group'] == "كروب B (بنات)")

st.write("### 🗂️ اضغطي على أي كروب أدناه لعرض طلابه فوراً:")

# أزرار الكروبات
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    if st.button(f"📁 كروب A (بنين)\n\n👥 الطلاب: {count_A}"):
        st.session_state.current_filter = "كروب A (بنين)"
with col2:
    if st.button(f"📁 كروب B (بنات)\n\n👥 الطلاب: {count_B}"):
        st.session_state.current_filter = "كروب B (بنات)"
with col3:
    if st.button("🔄 عرض الكل"):
        st.session_state.current_filter = "الكل"

st.write("---")

# 3. إضافة طالب جديد
with st.expander("➕ إضافة طالب جديد للمنظومة"):
    with st.form("add_student_form", clear_on_submit=True):
        new_name = st.text_input("اسم الطالب الثلاثي:")
        new_phone = st.text_input("رقم الهاتف:")
        new_group = st.selectbox("المجموعة / الكروب:", ["كروب A (بنين)", "كروب B (بنات)"])
        new_address = st.text_input("سكن الطالب (العنوان):")
        new_total = st.number_input("إجمالي قسط الدراسة:", min_value=0, value=1000)
        new_paid = st.number_input("المبلغ المدفوع حالياً (الواصل):", min_value=0, value=0)
        
        submit_btn = st.form_submit_button("حفظ بيانات الطالب")
        if submit_btn and new_name and new_phone:
            new_id = max([s['id'] for s in st.session_state.students]) + 1 if st.session_state.students else 1
            st.session_state.students.append({
                "id": new_id, "name": new_name, "phone": new_phone, 
                "group": new_group, "address": new_address, 
                "total_fee": new_total, "paid_fee": new_paid
            })
            st.success(f"تم إضافة الطالب {new_name} بنجاح!")
            st.rerun()

# 4. عرض الجدول المفصّل حسب اختياركِ
st.subheader(f"📋 قائمة الطلاب المعروضة حالياً: ({st.session_state.current_filter})")

if st.session_state.current_filter == "الكل":
    display_list = st.session_state.students
else:
    display_list = [s for s in st.session_state.students if s['group'] == st.session_state.current_filter]

if display_list:
    df = pd.DataFrame(display_list)
    df_display = df[["name", "phone", "group", "address"]].rename(columns={
        "name": "اسم الطالب", "phone": "رقم الهاتف", "group": "المجموعة / الكروب", "address": "السكن"
    })
    st.dataframe(df_display, use_container_width=True)
else:
    st.info("لا يوجد طلاب في هذا الكروب حالياً.")

# 5. إدارة حساب طالب (تعديل، حذف، أقساط، طباعة)
st.write("---")
st.subheader("🔍 استعراض وتعديل وإدارة حساب طالب")

all_names = [s['name'] for s in st.session_state.students]

if all_names:
    selected_student_name = st.selectbox("اختر اسم الطالب لإظهار ملفه المالي والشخصي:", all_names)
    student_idx = next(i for i, s in enumerate(st.session_state.students) if s['name'] == selected_student_name)
    student = st.session_state.students[student_idx]
    
    remaining_fee = student['total_fee'] - student['paid_fee']
    
    st.markdown(f"""
    <div class="student-card">
        <h4>📋 الملف الحالي للطالب: {student['name']}</h4>
        <p><b>📍 السكن والإقامة:</b> {student['address']} | <b>📞 رقم الهاتف:</b> {student['phone']} | <b>🗂️ الكروب:</b> {student['group']}</p>
        <hr style='border-color: #00adb5;'>
        <h5 style='color: #00adb5; margin-top:0;'>💰 الموقف المالي والتسديدات:</h5>
        <p>💵 <b>إجمالي القسط الكلي المطلـوب:</b> {student['total_fee']}</p>
        <p>🟢 <b style='color: #4caf50;'>المبلغ المدفوع (سـدّدني):</b> {student['paid_fee']}</p>
        <p>🔴 <b style='color: #f44336;'>المبلغ المتبقي بذمّته (بقت):</b> {remaining_fee}</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["💵 تسديد قسط وطباعة الوصل", "✏️ تعديل بيانات الطالب", "❌ حذف الطالب من المنظومة"])
    
    with tab1:
        pay_amount = st.number_input("أدخل المبلغ الواصل الآن:", min_value=0, value=0, step=50)
        if st.button("تسجيل واستلام المبلغ المالي"):
            if pay_amount > remaining_fee:
                st.error("⚠️ خطأ: المبلغ أكبر من المتبقي!")
            elif pay_amount > 0:
                st.session_state.students[student_idx]['paid_fee'] += pay_amount
                st.success("✅ تم تسجيل المبلغ بنجاح.")
                st.rerun()
                
        st.markdown('<div class="print-hint">🖨️ لطباعة الوصل: اضغطي على (Ctrl + P) في لوحة المفاتيح!</div>', unsafe_allow_html=True)
        
        receipt_html = f"""
        <div class="receipt-box">
            <h2 style="text-align: center; color: #00adb5; margin-top:0;">🎓 منظومة إدارة الطلاب 🎓</h2>
            <p style="text-align: center; font-size: 13px; color: #555;">وصل استلام مالي رسمي للطلبة</p>
            <hr style="border: 1px dashed #000000;">
            <p><b>اسم الطالب الثلاثي:</b> {student['name']}</p>
            <p><b>المجموعة / الكروب الدراسي:</b> {student['group']}</p>
            <p><b>منطقة السكن الحالية:</b> {student['address']}</p>
            <hr style="border: 1px dashed #000000;">
            <h3>📊 الموقف المالي المفصل:</h3>
            <p>• القسط الكلي الأساسي: <b>{student['total_fee']}</b></p>
            <p style="color: green;">• الواصل الكلي المدفوع (سـدّدني): <b>{student['paid_fee']}</b></p>
            <p style="color: red; font-weight: bold; font-size: 20px;">• المتبقي بذمّته (بقت): {remaining_fee}</p>
            <hr style="border: 1px dashed #000000;">
            <div style="margin-top: 35px; display: flex; justify-content: space-between; align-items: center;">
                <div><b>توقيع الحسابات:</b> ______________</div>
                <div style="border: 3px double red; padding: 6px 18px; color: red; font-weight: bold; transform: rotate(-4deg);">
                     ختم وتدقيق المنظومة <br> 🛑 تم التسديد المالي 🛑
                </div>
            </div>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)

    with tab2:
        edit_name = st.text_input("اسم الطالب الجديد الحقيقي:", value=student['name'])
        edit_phone = st.text_input("رقم الهاتف المعدل:", value=student['phone'])
        edit_address = st.text_input("تعديل منطقة السكن:", value=student['address'])
        edit_group = st.selectbox("تغيير الكروب الحالي:", ["كروب A (بنين)", "كروب B (بنات)"], index=["كروب A (بنين)", "كروب B (بنات)"].index(student['group']))
        edit_total = st.number_input("تعديل إجمالي القسط:", min_value=0, value=student['total_fee'])
        
        if st.button("تحديث وحفظ البيانات"):
            st.session_state.students[student_idx]['name'] = edit_name
            st.session_state.students[student_idx]['phone'] = edit_phone
            st.session_state.students[student_idx]['address'] = edit_address
            st.session_state.students[student_idx]['group'] = edit_group
            st.session_state.students[student_idx]['total_fee'] = edit_total
            st.success("✅ تم تحديث بيانات الطالب بنجاح!")
            st.rerun()

    with tab3:
        st.warning(f"انتبهي! هل تريدين حذف الطالب ({student['name']}) نهائياً؟")
        if st.button("تأكيد حذف الطالب ومسحه فوراً"):
            st.session_state.students.pop(student_idx)
            st.success("❌ تم حذف اسم الطالب من المنظومة.")
            st.rerun()
