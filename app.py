import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="NutriDNA AI - Stress & Sleep Edition", layout="centered")

st.title("🧠 NutriDNA AI")
st.subheader("AI phân tích thiếu ngủ & stress cho sinh viên")

st.header("Nhập thông tin của bạn")

age = st.number_input("Tuổi", 16, 30)
weight = st.number_input("Cân nặng (kg)", 40, 120)
height = st.number_input("Chiều cao (cm)", 140, 200)
if age < 18:
    st.info("⚠️ Kết quả chỉ mang tính tham khảo vì cơ thể vẫn đang phát triển.")
sleep = st.slider("Bạn ngủ bao nhiêu tiếng?", 0, 12)
stress = st.selectbox("Mức độ stress hôm nay", ["Thấp", "Trung bình", "Cao"])
# ===== Thông tin cá nhân mở rộng =====

goal = st.selectbox(
    "🎯 Mục tiêu hiện tại của bạn",
    ["Tăng năng lượng", "Giảm stress", "Giảm cân", "Tăng cân", "Duy trì sức khỏe"]
)

activity = st.selectbox(
    "🏃 Mức độ vận động",
    ["Ít vận động", "Vận động nhẹ", "Vận động nhiều"]
)

# ===== Dị ứng linh hoạt =====
allergies = st.multiselect(
    "🚫 Dị ứng / cần tránh",
    ["Sữa", "Hải sản", "Đậu phộng", "Gluten", "Trứng", "Đậu nành"]
)
# ===== Chọn phong cách thực đơn =====
menu_style = st.radio(
    "🍽 Chọn phong cách thực đơn",
    ["Món ăn Việt phổ biến", "Healthy / Fitness"]
)
# ===== DATABASE MÓN ĂN =====
menu = [
    {
        "name": "Bowl gạo lứt ức gà",
        "style": "Healthy / Fitness",
        "goal": ["Tăng năng lượng", "Giảm cân"],
        "contains": []
    },
    {
        "name": "Yến mạch chuối sữa",
        "style": "Healthy / Fitness",
        "goal": ["Giảm stress"],
        "contains": ["Sữa"]
    },
    {
        "name": "Cá hồi áp chảo",
        "style": "Healthy / Fitness",
        "goal": ["Tăng năng lượng"],
        "contains": ["Hải sản"]
    },
    {
        "name": "Salad đậu hũ",
        "style": "Healthy / Fitness",
        "goal": ["Giảm cân", "Giảm stress"],
        "contains": ["Đậu nành"]
    }
]

if st.button("Phân tích bằng AI"):

    recommended = []
    # ===== BMI =====
    if height > 0:
        bmi = weight / ((height/100) ** 2)
    else:
        st.error("Chiều cao không hợp lệ")
        st.stop()
    
    if bmi < 18.5:
        bmi_status = "Thiếu cân"
    elif bmi < 23:
        bmi_status = "Bình thường"
    elif bmi < 25:
        bmi_status = "Thừa cân"
    else:
        bmi_status = "Nguy cơ béo phì"

    # ===== Sleep Score =====
    sleep_score = min(sleep * 10, 100)

    if sleep < 5:
        sleep_status = "Nguy cơ suy giảm tập trung cao"
    elif sleep < 7:
        sleep_status = "Thiếu ngủ nhẹ"
    else:
        sleep_status = "Giấc ngủ tương đối ổn"

    # ===== Stress phân tích =====
    if stress == "Cao":
        stress_status = "Cortisol có thể đang cao"
    elif stress == "Trung bình":
        stress_status = "Cần hỗ trợ thư giãn nhẹ"
    else:
        stress_status = "Trạng thái tâm lý ổn định" 
    # ===== AI Impact Score =====
    if stress == "Thấp":
        stress_value = 20
    elif stress == "Trung bình":
        stress_value = 50
    else:
        stress_value = 80

    impact_score = (100 - sleep_score) * 0.6 + stress_value * 0.4 
    # ===== Cá nhân hóa nâng cao =====
    personal_factor = 0

    if goal == "Tăng năng lượng" and sleep < 6:
        personal_factor += 10

    if goal == "Giảm stress" and stress == "Cao":
        personal_factor += 10

    if activity == "Vận động nhiều":
        personal_factor += 5

    impact_score += personal_factor
    st.subheader("🧬 Kết quả phân tích AI")

    st.write(f"**BMI:** {round(bmi,1)} → {bmi_status}")
    st.write(f"**Sleep Score:** {sleep_score}/100 → {sleep_status}")
    st.progress(sleep_score / 100)
    if sleep_score < 50:
        st.error("🔴 Risk Level: Cao – Nguy cơ suy giảm tập trung và hiệu suất học tập.")
    elif sleep_score < 70:
        st.warning("🟡 Risk Level: Trung bình – Cần cải thiện giấc ngủ.")
    else:
        st.success("🟢 Risk Level: Thấp – Trạng thái tương đối ổn định.")

    st.caption("📊 Hệ thống sử dụng thuật toán đánh giá dựa trên chỉ số BMI, thời lượng ngủ       và mức độ stress tự báo cáo.")
    st.subheader("🧠 AI Impact Analysis")

    st.metric("Impact Score", round(impact_score,1))
    st.caption(f"AI đã điều chỉnh phân tích dựa trên mục tiêu '{goal}' và mức vận động '{activity}'.")

    if impact_score > 70:
        st.error("🔴 Tình trạng đáng lo ngại – Cần cải thiện giấc ngủ và giảm stress ngay.")
    elif impact_score > 40:
        st.warning("🟡 Có dấu hiệu ảnh hưởng đến hiệu suất học tập.")
    else:
        st.success("🟢 Ổn định – Tác động thấp đến sức khỏe tinh thần.")

    st.write(f"**Phân tích stress:** {stress_status}")

    # ===== BIỂU ĐỒ PHÂN TÍCH =====
    st.subheader("📊 Biểu đồ tác động")

    fig, ax = plt.subplots()

    labels = ["Thiếu ngủ", "Stress"]
    values = [100 - sleep_score, stress_value]

    bars = ax.bar(labels, values)

    ax.set_ylabel("Mức độ ảnh hưởng (%)")
    ax.set_ylim(0, 100)
    ax.set_title("So sánh mức độ tác động")

    # Thêm số trên đầu cột
    for i in range(len(values)):
        ax.text(i, values[i] + 2, str(round(values[i],1)), ha='center')

    st.pyplot(fig)
    st.info("🤖 AI phân tích rằng yếu tố có cột cao hơn đang ảnh hưởng mạnh hơn đến hiệu suất học tập của bạn.")
    if values[0] > values[1]:
        st.warning("👉 Ưu tiên cải thiện giấc ngủ trước.")
    else:
        st.warning("👉 Ưu tiên kiểm soát stress trước.")

    st.divider()

    st.subheader("🥗 Đề xuất dinh dưỡng phục hồi")

    recommended = []

    for item in menu:

        # 1. Lọc theo phong cách
        if item["style"] != menu_style:
            continue

        # 2. Lọc theo mục tiêu
        if goal not in item["goal"]:
            continue

        # 3. Lọc theo dị ứng (đa chọn)
        if any(allergy in item["contains"] for allergy in allergies):
            continue

        # ===== 4. TÍNH ĐIỂM =====
        score = 0

        # Trùng mục tiêu
        if goal in item["goal"]:
            score += 2

        # Ngủ ít → ưu tiên món tăng năng lượng
        if sleep < 6 and "Tăng năng lượng" in item["goal"]:
            score += 1

        # Stress cao → ưu tiên món giảm stress
        if stress == "Cao" and "Giảm stress" in item["goal"]:
            score += 1

        # Lưu vào danh sách
        recommended.append((item["name"], score))
    recommended.sort(key=lambda x: x[1], reverse=True)
    st.subheader("🏆 Top 3 món phù hợp nhất:")

    if recommended:
        for name, score in recommended[:3]:
            st.write(f"🥗 {name} — Điểm phù hợp: {score}")
    else:
        st.warning("Không tìm thấy món phù hợp.")

  
