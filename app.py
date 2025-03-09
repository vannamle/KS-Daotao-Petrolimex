import streamlit as st
import pandas as pd
from datetime import datetime

# Function to save survey responses to a CSV file
def save_response(data):
    df = pd.DataFrame([data])
    try:
        existing_data = pd.read_csv("survey_responses.csv", encoding='utf-8-sig')
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        # If file doesn't exist, create a new one
        pass
    df.to_csv("survey_responses.csv", index=False, encoding='utf-8-sig')

# Main chatbot function
def chatbot():
    st.title("Chatbot Khảo Sát Nhu Cầu Đào Tạo - Petrolimex")
    
    # Initialize session state if not already done
    if "step" not in st.session_state:
        st.session_state.step = 1
        st.session_state.responses = {}
    
    # Step 1: Personal Information
    if st.session_state.step == 1:
        st.subheader("Xin chào! Bạn vui lòng nhập thông tin cá nhân trước khi bắt đầu khảo sát.")
        name = st.text_input("Họ và Tên:")
        position = st.selectbox(
            "Chức vụ hiện tại:", 
            [
                "Phó Giám đốc", 
                "Kế toán trưởng", 
                "Trưởng phòng", 
                "Khác"
            ]
        )
        company = st.text_input("Công ty đang công tác:")
        experience = st.selectbox(
            "Số năm kinh nghiệm:", 
            [
                "< 3 năm", 
                "3 - 5 năm", 
                "5 - 10 năm", 
                "> 10 năm"
            ]
        )
        
        if st.button("Tiếp tục"):
            if not name or not company:
                st.warning("Vui lòng nhập đầy đủ Họ và Tên, Công ty trước khi tiếp tục! 🚀")
            else:
                st.session_state.responses.update({
                    "Tên": name, 
                    "Chức vụ": position, 
                    "Công ty": company, 
                    "Kinh nghiệm": experience,
                    "Thời gian khảo sát": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.session_state.step = 2
                st.rerun()  # Rerun to refresh the app state
    
    # Step 2: Self-Assessment of Knowledge
    elif st.session_state.step == 2:
        name = st.session_state.responses["Tên"]
        st.subheader(f"Cảm ơn bạn, {name}! Hãy đánh giá mức độ am hiểu của bạn.")
        st.subheader(f"(1: Chưa có kiến thức | 5: Rất thành thạo)")
        topics = [
            "Chiến lược và quản trị doanh nghiệp", 
            "Quản lý tài chính và dòng tiền",
            "Quản lý nhân sự và phát triển đội ngũ", 
            "Ứng dụng công nghệ và đổi mới sáng tạo",
            "Quản trị chuỗi cung ứng trong ngành xăng dầu", 
            "Kỹ năng lãnh đạo và ra quyết định",
            "Quản trị rủi ro trong ngành xăng dầu"
        ]
        ratings = {}
        for topic in topics:
            ratings[topic] = st.slider(topic, 1, 5, 3, key=topic)  # Added unique key for each slider
        
        if st.button("Tiếp tục"):
            st.session_state.responses.update(ratings)
            
            # Determine chatbot response based on ratings
            if all(value <= 2 for value in ratings.values()):
                st.session_state.responses["Chatbot phản hồi"] = f"Đừng lo, {name}! Chương trình đào tạo sẽ giúp bạn nâng cao năng lực! 💪"
            elif all(value >= 4 for value in ratings.values()):
                st.session_state.responses["Chatbot phản hồi"] = f"Bạn có nền tảng rất tốt, {name}! Chương trình sẽ giúp bạn hoàn thiện kỹ năng hơn nữa! 🚀"
            else:
                st.session_state.responses["Chatbot phản hồi"] = f"Bạn có kiến thức tốt ở một số lĩnh vực! Chúng tôi sẽ giúp bạn phát triển thêm những kỹ năng cần thiết! 🎯"
            
            st.session_state.step = 3
            st.rerun()
    
    # Step 3: Training Needs
    elif st.session_state.step == 3:
        name = st.session_state.responses["Tên"]
        st.subheader(f"{name}, bạn mong muốn đào tạo về lĩnh vực nào?")
        training_needs = st.multiselect(
            "Chọn tối đa 3 lĩnh vực:", 
            [
                "Chiến lược và quản trị doanh nghiệp", 
                "Quản lý tài chính và dòng tiền", 
                "Quản lý nhân sự", 
                "Ứng dụng công nghệ", 
                "Quản trị chuỗi cung ứng", 
                "Kỹ năng lãnh đạo", 
                "Quản trị rủi ro"
            ], 
            max_selections=3
        )
        custom_training = st.text_input("Bạn có mong muốn đào tạo về lĩnh vực khác không?")
        format_preference = st.selectbox(
            "Hình thức đào tạo mong muốn:", 
            [
                "Học trực tiếp", 
                "Học trực tuyến", 
                "Học kết hợp"
            ]
        )
        external_activities = st.multiselect(
            "Hoạt động bổ trợ:", 
            [
                'Case study thực tế',
                'Workshop, thảo luận nhóm',
                'Tham quan doanh nghiệp',
                'Coaching 1:1 với chuyên gia'          
            ],
        )
        
        if st.button("Tiếp tục"):
            st.session_state.responses.update({
                "Nhu cầu đào tạo": training_needs, 
                "Nội dung khác": custom_training, 
                "Hình thức đào tạo": format_preference,
                'Hoạt động bổ trợ': external_activities
            })
            st.session_state.step = 4
            st.rerun()
    
    # Step 4: Training Difficulties
    elif st.session_state.step == 4:
        name = st.session_state.responses["Tên"]
        st.subheader(f"{name}, bạn gặp khó khăn gì trong việc tham gia đào tạo?")
        difficulties = st.multiselect(
            "Chọn tất cả những yếu tố phù hợp:", 
            [
                "Công việc bận rộn", 
                "Địa điểm đào tạo xa", 
                "Chương trình không phù hợp", 
                "Không có thời gian học trực tuyến", 
                "Khác"
            ]
        )

        other_difficulty = st.text_input("Khó khăn khác:")
        
        if "Công việc bận rộn" in difficulties:
            st.write("Chúng tôi sẽ cố gắng thiết kế chương trình linh hoạt nhất có thể để hỗ trợ bạn! 🎯")

        respondent_suggestion = st.text_input("Theo bạn, chương trình đào tạo này có thể cải thiện hoặc bổ sung điều gì để hiệu quả hơn? ✍️")
        
        if st.button("Hoàn thành khảo sát"):
            st.session_state.responses.update(
                {
                    "Khó khăn": difficulties, 
                    'Khó khăn khác': other_difficulty,
                    'Góp ý': respondent_suggestion
                }
            )
            save_response(st.session_state.responses)
            st.session_state.step = 5
            st.rerun()
    
    # Step 5: Survey Completion
    elif st.session_state.step == 5:
        name = st.session_state.responses["Tên"]
        st.success(f"Cảm ơn bạn, {name}! Khảo sát đã hoàn thành. 🚀")
        st.write("Dữ liệu của bạn đã được ghi nhận thành công.")
        
        # Reset survey with a button
        if st.button("Khảo sát lại"):
            st.session_state.step = 1
            st.session_state.responses = {}
            st.rerun()

if __name__ == "__main__":
    chatbot()