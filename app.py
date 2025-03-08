import streamlit as st
import pandas as pd
from datetime import datetime

def save_response(data):
    df = pd.DataFrame([data])
    try:
        existing_data = pd.read_csv("survey_responses.csv")
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv("survey_responses.csv", index=False)

def chatbot():
    st.title("Chatbot Khảo Sát Nhu Cầu Đào Tạo - Petrolimex")
    
    if "step" not in st.session_state:
        st.session_state.step = 1
        st.session_state.responses = {}
    
    if st.session_state.step == 1:
        st.subheader("Xin chào! Bạn vui lòng nhập thông tin cá nhân trước khi bắt đầu khảo sát.")
        name = st.text_input("Họ và Tên:")
        position = st.selectbox("Chức vụ hiện tại:", ["Phó Giám đốc", "Kế toán trưởng", "Trưởng phòng", "Khác"])
        company = st.text_input("Công ty đang công tác:")
        experience = st.selectbox("Số năm kinh nghiệm:", ["< 3 năm", "3 - 5 năm", "5 - 10 năm", "> 10 năm"])
        
        if st.button("Tiếp tục") and name:
            st.session_state.responses.update({
                "Tên": name, "Chức vụ": position, "Công ty": company, "Kinh nghiệm": experience,
                "Thời gian khảo sát": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.session_state.step = 2
            st.experimental_rerun()
    
    elif st.session_state.step == 2:
        st.subheader(f"Cảm ơn bạn, {st.session_state.responses['Tên']}! Hãy đánh giá mức độ am hiểu của bạn.")
        topics = [
            "Chiến lược và quản trị doanh nghiệp", "Quản lý tài chính và dòng tiền",
            "Quản lý nhân sự và phát triển đội ngũ", "Ứng dụng công nghệ và đổi mới sáng tạo",
            "Quản trị chuỗi cung ứng trong ngành xăng dầu", "Kỹ năng lãnh đạo và ra quyết định",
            "Quản trị rủi ro trong ngành xăng dầu"
        ]
        ratings = {}
        for topic in topics:
            ratings[topic] = st.slider(topic, 1, 5, 3)
        
        if st.button("Tiếp tục"):
            st.session_state.responses.update(ratings)
            st.session_state.step = 3
            st.experimental_rerun()
    
    elif st.session_state.step == 3:
        st.subheader(f"{st.session_state.responses['Tên']}, bạn mong muốn đào tạo về lĩnh vực nào?")
        training_needs = st.multiselect(
            "Chọn tối đa 3 lĩnh vực:", 
            ["Chiến lược và quản trị doanh nghiệp", "Quản lý tài chính và dòng tiền", "Quản lý nhân sự", 
             "Ứng dụng công nghệ", "Quản trị chuỗi cung ứng", "Kỹ năng lãnh đạo", "Quản trị rủi ro"], 
            max_selections=3
        )
        custom_training = st.text_input("Bạn có mong muốn đào tạo về lĩnh vực khác không?")
        format_preference = st.selectbox("Hình thức đào tạo mong muốn:", ["Học trực tiếp", "Học trực tuyến", "Học kết hợp"])
        
        if st.button("Tiếp tục"):
            st.session_state.responses.update({"Nhu cầu đào tạo": training_needs, "Nội dung khác": custom_training, "Hình thức đào tạo": format_preference})
            st.session_state.step = 4
            st.experimental_rerun()
    
    elif st.session_state.step == 4:
        st.subheader(f"{st.session_state.responses['Tên']}, bạn gặp khó khăn gì trong việc tham gia đào tạo?")
        difficulties = st.multiselect(
            "Chọn tất cả những yếu tố phù hợp:", 
            ["Công việc bận rộn", "Địa điểm đào tạo xa", "Chương trình không phù hợp", "Không có thời gian học trực tuyến", "Khác"]
        )
        difficulty_details = st.text_input("Nếu có lý do khác, vui lòng nhập vào đây:")
        feedback = st.text_area("Bạn có ý kiến đóng góp gì để chương trình hiệu quả hơn?")
        
        if st.button("Hoàn thành khảo sát"):
            st.session_state.responses.update({"Khó khăn": difficulties, "Lý do khác": difficulty_details, "Đóng góp": feedback})
            save_response(st.session_state.responses)
            st.session_state.step = 5
            st.experimental_rerun()
    
    elif st.session_state.step == 5:
        st.success(f"Cảm ơn bạn, {st.session_state.responses['Tên']}! Khảo sát đã hoàn thành. 🚀")
        st.write("Dữ liệu của bạn đã được ghi nhận thành công.")
        st.button("Khảo sát lại", on_click=lambda: st.session_state.update(step=1, responses={}))

if __name__ == "__main__":
    chatbot()
