import streamlit as st
import openai

# Nhập API Key của OpenAI
openai.api_key = "YOUR_OPENAI_API_KEY"

# Giao diện chính
st.title("📋 Khảo sát nhu cầu đào tạo CEO - Petrolimex")

# Giới thiệu mục tiêu khảo sát
st.write("""
Chào mừng bạn đến với khảo sát nhu cầu đào tạo dành cho cán bộ nguồn của Petrolimex. 

**Mục tiêu**: Chúng tôi mong muốn hiểu rõ hơn về nhu cầu đào tạo của bạn để thiết kế một chương trình phù hợp.

**Bảo mật thông tin**: Mọi thông tin bạn cung cấp sẽ được bảo mật và chỉ sử dụng cho mục đích nghiên cứu.

Hãy nhập tên của bạn để bắt đầu!
""")

# Thu thập thông tin nhân khẩu học
def chatbot_interview():
    if 'name' not in st.session_state:
        st.session_state['name'] = ""
    
    st.session_state['name'] = st.text_input("📌 Nhập họ và tên của bạn:", value=st.session_state['name'])
    
    if st.session_state['name']:
        st.write(f"Cảm ơn {st.session_state['name']}! Hãy tiếp tục với khảo sát nhé.")
        
        # Câu hỏi 1: Chức danh công tác
        position = st.selectbox("📌 Chức danh hiện tại của bạn:", ["Phó Giám đốc", "Kế toán trưởng", "Trưởng phòng", "Khác"])
        
        # Câu hỏi 2: Đơn vị công tác
        company = st.text_input("📌 Đơn vị công tác:")
        
        # Câu hỏi 3: Số năm kinh nghiệm
        experience = st.slider("📌 Số năm kinh nghiệm làm việc:", 1, 30, 5)
        
        if st.button("Tiếp tục khảo sát"):
            st.session_state['info_collected'] = True
            st.experimental_rerun()
    
if 'info_collected' not in st.session_state:
    chatbot_interview()
else:
    st.write(f"Cảm ơn {st.session_state['name']}! Bạn đã hoàn thành phần thu thập thông tin cá nhân. Tiếp theo, chatbot sẽ phỏng vấn bạn về nhu cầu đào tạo.")
