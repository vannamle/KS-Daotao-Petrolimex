import streamlit as st
import openai

# Nhập API Key của OpenAI (Lưu ý: KHÔNG chia sẻ khóa này)
openai.api_key = "YOUR_OPENAI_API_KEY"

st.title("🤖 AI Interview Chatbot")
st.write("Chào mừng bạn đến với Chatbot phỏng vấn AI! Hãy nhập câu hỏi của bạn bên dưới.")

# Tạo danh sách câu hỏi có sẵn
questions = [
    "Tell me about yourself.",
    "What are your greatest strengths?",
    "What are your weaknesses?",
    "Why do you want to work here?",
    "Where do you see yourself in 5 years?",
]

# Chọn câu hỏi ngẫu nhiên từ danh sách hoặc nhập tay
question = st.selectbox("Chọn một câu hỏi", ["Tự nhập câu hỏi"] + questions)

if question == "Tự nhập câu hỏi":
    question = st.text_input("Nhập câu hỏi của bạn:")

if st.button("Hỏi Chatbot"):
    if question:
        with st.spinner("Chatbot đang suy nghĩ... 💭"):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "Bạn là một nhà tuyển dụng chuyên nghiệp."},
                          {"role": "user", "content": question}]
            )
            answer = response['choices'][0]['message']['content']
            st.write("💬 **Chatbot trả lời:**", answer)
    else:
        st.warning("Vui lòng nhập câu hỏi!")