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
        
        if st.button("Tiếp tục"):
            if not name or not company:
                st.warning("Vui lòng nhập đầy đủ Họ và Tên, Công ty trước khi tiếp tục! 🚀")
            else:
                st.session_state.responses.update({
                    "Tên": name, "Chức vụ": position, "Công ty": company, "Kinh nghiệm": experience,
                    "Thời gian khảo sát": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.session_state.step = 2
                st.rerun()
    
    elif st.session_state.step == 2:
        name = st.session_state.responses["Tên"]
        st.subheader(f"Cảm ơn bạn, {name}! Hãy đánh giá mức độ am hiểu của bạn.")
        topics = [
            "Chiến lược và quản trị doanh nghiệp", "Quản lý tài chính và dòng tiền",
            "Quản lý nhân sự và phát triển đội ngũ", "Ứng dụng công nghệ và đổi mới sáng tạo",
            "Quản trị chuỗi cung ứng trong ngành xăng dầu", "Kỹ năng lãnh đạo và ra quyết định",
            "Quản trị rủi ro trong ngành xăng dầu"
        ]
        ratings = {}
        for topic in topics:
            rating = st.slider(topic, 1, 5, 3)
            ratings[topic] = rating
        
        if st.button("Tiếp tục"):
            st.session_state.responses.update(ratings)
            
            if all(value <= 2 for value in ratings.values()):
                st.session_state.responses["Chatbot phản hồi"] = "Đừng lo, {name}! Chương trình đào tạo sẽ giúp bạn nâng cao năng lực! 💪"
            elif all(value >= 4 for value in ratings.values()):
                st.session_state.responses["Chatbot phản hồi"] = "Bạn có nền tảng rất tốt, {name}! Chương trình sẽ giúp bạn hoàn thiện kỹ năng hơn nữa! 🚀"
            else:
                st.session_state.responses["Chatbot phản hồi"] = "Bạn có kiến thức tốt ở một số lĩnh vực! Chúng tôi sẽ giúp bạn phát triển thêm những kỹ năng cần thiết! 🎯"
            
            st.session_state.step = 3
            st.rerun()
    
    elif st.session_state.step == 3:
        name = st.session_state.responses["Tên"]
        st.subheader(f"{name}, bạn mong muốn đào tạo về lĩnh vực nào?")
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
            st.rerun()
    
    elif st.session_state.step == 4:
        name = st.session_state.responses["Tên"]
        st.subheader(f"{name}, bạn gặp khó khăn gì trong việc tham gia đào tạo?")
        difficulties = st.multiselect(
            "Chọn tất cả những yếu tố phù hợp:", 
            ["Công việc bận rộn", "Địa điểm đào tạo xa", "Chương trình không phù hợp", "Không có thời gian học trực tuyến", "Khác"]
        )
        
        if "Công việc bận rộn" in difficulties:
            st.write("Chúng tôi sẽ cố gắng thiết kế chương trình linh hoạt nhất có thể để hỗ trợ bạn! 🎯")
        
        if st.button("Hoàn thành khảo sát"):
            st.session_state.responses.update({"Khó khăn": difficulties})
            save_response(st.session_state.responses)
            st.session_state.step = 5
            st.rerun()
    
    elif st.session_state.step == 5:
        name = st.session_state.responses["Tên"]
        st.success(f"Cảm ơn bạn, {name}! Khảo sát đã hoàn thành. 🚀")
        st.write("Dữ liệu của bạn đã được ghi nhận thành công.")
        st.button("Khảo sát lại", on_click=lambda: st.session_state.update(step=1, responses={}))

if __name__ == "__main__":
    chatbot()
