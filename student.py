import streamlit as st
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="منظومة إدارة الطلاب", page_icon="🎓", layout="wide")

# تصميم المظهر المخصص (CSS)
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
        background-color: #ffffff;
        color: #000000;
        padding: 25px;
        border-radius: 8px;
        border: 2px dashed #000000;
        font-family: 'Arial', sans-serif;
        margin-top: 15px;
    }
    /* تأثيرات عند الضغط على أزرار الطباعة */
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

# 1. نظام تخزين البيانات في الذاكرة
if "students" not in st.session_state:
    st.session_state.students = [
        {"id": 1, "name": "أحمد علي", "phone": "7709971745", "group": "(بنين) A كروب", "address": "الموصل - الزهور", "total_fee": 1000, "paid_fee": 400},
        {"id": 2, "name": "محمد جاسم", "phone": "5413524151", "group": "(بنين) A كروب", "address": "الموصل - المهندسين", "total_fee": 1200, "paid_fee": 600}
    ]

st.title("🎓 منظومة إدارة شؤون الطلاب والأقساط")

# 2. بطاقات العدادات العلوية للكروبات
group_A_count = sum(1 for s in st.session_state.students if s['group'] == "(بنين) A كروب")
group_B_count = sum(1 for s in st.session_state.students if s['group'] == "كروب B (بنات)")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="group-box"><h3>(بنين) A كروب 📂</h3><p style="font-size:24px;">الطلاب: {group_A_count} 👥</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="group-box"><h3>كروب B (بنات) 📂</h3><p style="font-size:24px;">الطلاب: {group_B_count} 👥</p></div>', unsafe_allow_html=True)

# 3. قسم إضافة طالب جديد للمنظومة
with st.expander("➕ إضافة طالب جديد للمنظومة"):
    with st.form("add_student_form", clear_on_submit=True):
        new_name = st.text_input("اسم الطالب الثلاثي:")
        new_phone = st.text_input("رقم الهاتف:")
        new_group = st.selectbox("المجموعة / الكروب:", ["(بنين) A كروب", "كروب B (بنات)"])
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

# 4. عرض جدول الطلاب العام
st.subheader("📋 قائمة الطلاب المسجلين")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    df_display = df[["name", "phone", "group", "address"]].rename(columns={
        "name": "اسم الطالب", "phone": "رقم الهاتف", "group": "المجموعة / الكروب", "address": "السكن"
    })
    st.dataframe(df_display, use_container_width=True)
else:
    st.info("لا يوجد طلاب مسجلين حالياً.")

# 5. قسم إدارة واختيار طالب لتعديل بياناته أو حذفه أو طباعة وصله
st.subheader("🔍 استعراض وتعديل وإدارة حساب طالب")
student_names = [s['name'] for s in st.session_state.students]

if student_names:
    selected_student_name = st.selectbox("اختر اسم الطالب لإظهار ملفه المالي والشخصي:", student_names)
    student_idx = next(i for i, s in enumerate(st.session_state.students) if s['name'] == selected_student_name)
    student = st.session_state.students[student_idx]
    
    # حساب القسط المتبقي تلقائياً
    remaining_fee = student['total_fee'] - student['paid_fee']
    
    # عرض كارت الطالب الملون
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
    
    # تبويبات العمليات المتاحة
    tab1, tab2, tab3 = st.tabs(["💵 تسديد قسط وطباعة الوصل", "✏️ تعديل بيانات الطالب", "❌ حذف الطالب من المنظومة"])
    
    with tab1:
        st.write("### 🧾 دفع مبلغ جديد وتجهيز الوصل للطباعة")
        pay_amount = st.number_input("أدخل المبلغ الواصل الآن:", min_value=0, value=0, step=50)
        if st.button("تسجيل واستلام المبلغ المالي"):
            if pay_amount > remaining_fee:
                st.error("⚠️ خطأ: المبلغ المدفوع أكبر من المتبقي على الطالب!")
            elif pay_amount > 0:
                st.session_state.students[student_idx]['paid_fee'] += pay_amount
                st.success(f"✅ تم تسجيل {pay_amount} بنجاح في حساب الطالب المالي.")
                st.rerun()
                
        st.write("---")
        st.markdown('<div class="print-hint">🖨️ لطباعة الوصل أدناه: اضغطي على أزرار (Ctrl + P) معاً في لوحة المفاتيح لتفتح لكِ نافذة الطباعة الفورية وجاهزة الختم!</div>', unsafe_allow_html=True)
        
        # تصميم شكل الوصل الرسمي والملون داخل البرنامج
        receipt_html = f"""
        <div class="receipt-box">
            <h2 style="text-align: center; color: #00adb5; margin-bottom: 5px; margin-top:0;">🎓 منظومة إدارة الطلاب 🎓</h2>
            <p style="text-align: center; font-size: 13px; color: #555;">وصل استلام مالي رسمي للطلبة</p>
            <hr style="border: 1px dashed #000000;">
            <p style="font-size:16px;"><b>اسم الطالب الثلاثي:</b> {student['name']}</p>
            <p style="font-size:16px;"><b>المجموعة / الكروب الدراسي:</b> {student['group']}</p>
            <p style="font-size:16px;"><b>منطقة السكن الحالية:</b> {student['address']}</p>
            <hr style="border: 1px dashed #000000;">
            <h3 style="color: #000000; margin-top:10px;">📊 الموقف المالي المفصل:</h3>
            <p style="font-size:16px;">• القسط الكلي الأساسي: <b>{student['total_fee']}</b></p>
            <p style="font-size:16px; color: green;">• الواصل الكلي المدفوع (سـدّدني): <b>{student['paid_fee']}</b></p>
            <p style="font-size:20px; color: red; font-weight: bold;">• المتبقي بذمّته (بقت): {remaining_fee}</p>
            <hr style="border: 1px dashed #000000;">
            <div style="margin-top: 35px; display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size:15px;"><b>توقيع الحسابات:</b> ______________</div>
                <div style="text-align: center; border: 3px double red; padding: 6px 18px; border-radius: 5px; color: red; font-weight: bold; font-size: 16px; transform: rotate(-4deg);">
                     ختم وتدقيق المنظومة <br> 🛑 تم التسديد المالي 🛑
                </div>
            </div>
        </div>
        """
        st.markdown(receipt_html, unsafe_allow_html=True)

    with tab2:
        st.write("### ✏️ تعديل المعلومات الشخصية للطالب")
        edit_name = st.text_input("اسم الطالب الجديد الحقيقي:", value=student['name'])
        edit_phone = st.text_input("رقم الهاتف المعدل:", value=student['phone'])
        edit_address = st.text_input("تعديل منطقة السكن:", value=student['address'])
        edit_group = st.selectbox("تغيير الكروب الحالي:", ["(بنين) A كروب", "كروب B (بنات)"], index=["(بنين) A كروب", "كروب B (بنات)"].index(student['group']))
        edit_total = st.number_input("تعديل إجمالي القسط:", min_value=0, value=student['total_fee'])
        
        if st.button("تحديث وحفظ البيانات الشخصية والمالية"):
            st.session_state.students[student_idx]['name'] = edit_name
            st.session_state.students[student_idx]['phone'] = edit_phone
            st.session_state.students[student_idx]['address'] = edit_address
            st.session_state.students[student_idx]['group'] = edit_group
            st.session_state.students[student_idx]['total_fee'] = edit_total
            st.success("✅ تم تحديث وتغيير كافة معلومات الطالب بنجاح!")
            st.rerun()

    with tab3:
        st.write("### ⚠️ منطقة حذف الطلاب")
        st.warning(f"انتبهي! هل أنتِ متأكدة من رغبتكِ بحذف ملف الطالب ({student['name']}) نهائياً من سجل الحسابات؟")
        if st.button("تأكيد حذف الطالب ومسحه فوراً"):
            st.session_state.students.pop(student_idx)
            st.success("❌ تم مسح وحذف اسم الطالب من المنظومة.")
            st.rerun()
