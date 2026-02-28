import os
import time
import streamlit as st
import matplotlib.pyplot as plt
import unicodedata
import re
st.set_page_config(
    page_title="NutriDNA AI",
    page_icon="🧬",
    layout="wide"
)
st.markdown("""
<style>
.hero-title {
    font-size: 72px;
    font-weight: 900;
    position: relative;
    display: inline-block;
    overflow: hidden;

    /* Gradient chữ */
    background: linear-gradient(90deg, #00f5d4, #00bbf9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    /* Glow phát sáng */
    text-shadow:
        0 0 10px rgba(0,255,220,0.6),
        0 0 20px rgba(0,255,220,0.5),
        0 0 40px rgba(0,255,220,0.4);

    animation: glowPulse 3s ease-in-out infinite;
}

/* Hiệu ứng glow nhịp thở */
@keyframes glowPulse {
    0% {
        text-shadow:
            0 0 10px rgba(0,255,220,0.4),
            0 0 20px rgba(0,255,220,0.3),
            0 0 30px rgba(0,255,220,0.2);
    }
    50% {
        text-shadow:
            0 0 20px rgba(0,255,220,0.8),
            0 0 40px rgba(0,255,220,0.6),
            0 0 60px rgba(0,255,220,0.4);
    }
    100% {
        text-shadow:
            0 0 10px rgba(0,255,220,0.4),
            0 0 20px rgba(0,255,220,0.3),
            0 0 30px rgba(0,255,220,0.2);
    }
}

/* Shine quét ngang */
.hero-title::after {
    content: "";
    position: absolute;
    top: 0;
    left: -150%;
    width: 50%;
    height: 100%;
    background: linear-gradient(
        120deg,
        rgba(255,255,255,0) 0%,
        rgba(255,255,255,0.9) 50%,
        rgba(255,255,255,0) 100%
    );
    transform: skewX(-25deg);
    animation: shine 4s infinite;
}

@keyframes shine {
    0% { left: -150%; }
    100% { left: 200%; }
}
.hero-title::after {
    content: "";
    position: absolute;
    top: 0;
    left: -150%;
    width: 50%;
    height: 100%;
    background: linear-gradient(
        120deg,
        rgba(255,255,255,0) 0%,
        rgba(255,255,255,0.9) 50%,
        rgba(255,255,255,0) 100%
    );
    transform: skewX(-25deg);
    animation: shine 4s infinite;
}

@keyframes shine {
    0% { left: -150%; }
    100% { left: 200%; }
}

.hero-subtitle {
    font-size: 28px;
    font-weight: 700;
    margin-top: 20px;
    color: #00e6c3;

    text-shadow:
        0 0 10px rgba(0,255,200,0.6),
        0 0 20px rgba(0,255,200,0.4);

    animation: subtitleGlow 3s ease-in-out infinite;
}

@keyframes subtitleGlow {
    0% {
        text-shadow:
            0 0 6px rgba(0,255,200,0.4),
            0 0 12px rgba(0,255,200,0.3);
    }
    50% {
        text-shadow:
            0 0 14px rgba(0,255,200,0.7),
            0 0 25px rgba(0,255,200,0.5);
    }
    100% {
        text-shadow:
            0 0 6px rgba(0,255,200,0.4),
            0 0 12px rgba(0,255,200,0.3);
    }
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="glass-hero">

<div class="hero-title">
🧬 NutriDNA AI
</div>

<div class="hero-subtitle">
AI phân tích thiếu ngủ & stress để gợi ý thực đơn cá nhân hóa
</div>

</div>
""", unsafe_allow_html=True)
# ===== CẤU HÌNH THƯ MỤC ẢNH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
images = os.path.join(BASE_DIR, "images")
def calculate_tdee(weight, height, age, gender, activity_level):

    if gender == "Nam":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multipliers = {
        "Ít vận động": 1.2,
        "Vận động nhẹ": 1.375,
        "Vận động vừa": 1.55,
        "Vận động nhiều": 1.725
    }

    return bmr * activity_multipliers.get(activity_level, 1.2)
def normalize_name(name):
    # chuyển đ → d trước
    name = name.replace("đ", "d").replace("Đ", "D")

    # bỏ dấu
    name = unicodedata.normalize('NFD', name)
    name = name.encode('ascii', 'ignore').decode('utf-8')

    # viết thường
    name = name.lower()

    # thay & bằng khoảng trắng
    name = name.replace("&", " ")

    # bỏ ký tự đặc biệt
    name = re.sub(r'[^a-z0-9\s]', '', name)

    # gộp nhiều khoảng trắng thành 1
    name = re.sub(r'\s+', ' ', name)

    # thay khoảng trắng bằng _
    name = name.replace(" ", "_")

    return name

st.markdown("""
<style>
.main {
    background-color: #f4f8f7;
}

h1, h2, h3 {
    color: #0d5c63;
}

div.stButton > button {
    background: linear-gradient(90deg, #00f5d4, #00bbf9);
    color: white;
    border-radius: 16px;
    padding: 14px 32px;
    font-weight: bold;
    border: none;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

div.stButton > button::after {
    content: "";
    position: absolute;
    top: 0;
    left: -150%;
    width: 50%;
    height: 100%;
    background: linear-gradient(
        120deg,
        rgba(255,255,255,0) 0%,
        rgba(255,255,255,0.8) 50%,
        rgba(255,255,255,0) 100%
    );
    transform: skewX(-25deg);
    animation: buttonShine 3s infinite;
}

@keyframes buttonShine {
    0% { left: -150%; }
    100% { left: 200%; }
}

div.stButton > button:hover {
    transform: translateY(-4px);
}
div.stMetric {
    background: rgba(255,255,255,0.8);
    padding: 25px;
    border-radius: 25px;

    backdrop-filter: blur(20px);

    border: 1px solid rgba(255,255,255,0.6);

    box-shadow:
        0 20px 50px rgba(0,0,0,0.08),
        0 0 40px rgba(0,255,200,0.1);

    transition: all 0.3s ease;
}

div.stMetric:hover {
    transform: translateY(-5px);
    box-shadow:
        0 30px 60px rgba(0,0,0,0.12),
        0 0 60px rgba(0,255,200,0.2);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ===== NỀN TOÀN TRANG ===== */
.stApp {
    background:
        radial-gradient(circle at 20% 30%, rgba(0,255,200,0.25), transparent 45%),
        radial-gradient(circle at 80% 70%, rgba(0,180,255,0.25), transparent 45%),
        linear-gradient(135deg, #f0fbff 0%, #f7fcff 50%, #ffffff 100%);
    animation: bgShift 12s ease-in-out infinite alternate;
}

@keyframes bgShift {
    from { filter: brightness(1); }
    to { filter: brightness(1.05); }
}
/* ===== HERO GLASS ===== */
.glass-hero {
    position: relative;
    text-align: center;

    padding: 160px 40px;
    margin: 80px auto;
    max-width: 1100px;

    background: rgba(255,255,255,0.4);
    backdrop-filter: blur(40px);
    -webkit-backdrop-filter: blur(40px);

    border-radius: 50px;
    border: 1px solid rgba(255,255,255,0.6);

    box-shadow:
        0 50px 120px rgba(0,0,0,0.1),
        0 0 120px rgba(0,255,200,0.2);

    animation: heroEnter 1.2s ease-out forwards;
    opacity: 0;
    transform: translateY(50px);
}

@keyframes heroEnter {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("https://www.transparenttextures.com/patterns/cubes.png");
    opacity: 0.03;
    z-index: -1;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Track nền */
div[data-baseweb="slider"] > div {
    background: linear-gradient(
        90deg,
        rgba(0,198,255,0.15),
        rgba(0,114,255,0.15)
    );
    border-radius: 20px;
    height: 8px;
}

/* Thanh active */
div[data-baseweb="slider"] div[role="presentation"] {
    border-radius: 20px;
    height: 8px;
}

/* Nút tròn */
div[data-baseweb="slider"] [role="slider"] {
    background-color: white;
    border: 3px solid #0072ff;
    width: 18px;
    height: 18px;
    box-shadow: 0 0 10px rgba(0,114,255,0.4);
}

</style>
""", unsafe_allow_html=True)

st.header("📋 Nhập thông tin của bạn")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Tuổi", 16, 30)

    gender = st.selectbox(
        "Giới tính",
        ["Nam", "Nữ"]
    )

    weight = st.number_input("Cân nặng (kg)", 40, 120)
    height = st.number_input("Chiều cao (cm)", 140, 200)
    allergies = st.multiselect(
        "Dị ứng / cần tránh",
        ["Sữa", "Hải sản", "Đậu phộng", "Gluten", "Trứng", "Đậu nành"]
    )

with col2:
    goal = st.selectbox(
        "Mục tiêu hiện tại của bạn",
        ["Tăng năng lượng", "Giảm stress", "Giảm cân", "Tăng cân", "Duy trì sức khỏe"]
    )

    activity_level = st.selectbox(
      "Mức độ vận động",
      [
        "Ít vận động",
        "Vận động nhẹ",
        "Vận động vừa",
        "Vận động nhiều"
      ]
    )
    st.markdown("### 🧠 Trạng thái thần kinh hôm nay")
    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
    sleep = st.slider("Bạn ngủ bao nhiêu tiếng?", 3, 10, 7)
    if sleep < 6:
        st.warning("🧠 Cơ thể đang thiếu phục hồi thần kinh.")
    elif sleep < 8:
        st.info("⚖ Giấc ngủ ở mức ổn định.")
    else:
        st.success("🚀 Phục hồi tối ưu cho não bộ.")
    st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)
    stress = st.slider("Mức độ stress hôm nay", 1, 10, 5)
    if stress >= 8:
       st.error("⚠ Cortisol có thể đang ở mức cao.")
    elif stress >= 5:
       st.warning("📊 Stress trung bình.")
    else:
       st.success("🌿 Hệ thần kinh đang cân bằng.")
    st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)

   
# ===== DATABASE MÓN ĂN =====
foods = [

    {"name": "Cơm lứt bò áp chảo", "calories": 520, "protein": 35, "carbs": 55, "fat": 18},
    {"name": "Cơm lứt gà nướng mật ong", "calories": 480, "protein": 38, "carbs": 60, "fat": 9},
    {"name": "Cơm lứt tôm áp chảo", "calories": 450, "protein": 32, "carbs": 58, "fat": 7},
    {"name": "Cơm lứt ức gà sốt pesto", "calories": 510, "protein": 40, "carbs": 50, "fat": 18},

    {"name": "Cháo yến mạch hạt óc chó", "calories": 380, "protein": 12, "carbs": 45, "fat": 18},
    {"name": "Pasta nguyên cám ức gà", "calories": 520, "protein": 42, "carbs": 65, "fat": 10},

    {"name": "Salad bò cá hồi", "calories": 500, "protein": 38, "carbs": 20, "fat": 35},
    {"name": "Salad cá ngừ Địa Trung Hải", "calories": 420, "protein": 35, "carbs": 18, "fat": 22},
    {"name": "Salad đậu hũ", "calories": 350, "protein": 22, "carbs": 20, "fat": 20},
    {"name": "Salad đậu lăng", "calories": 380, "protein": 20, "carbs": 45, "fat": 10},
    {"name": "Salad ức gà mè rang", "calories": 460, "protein": 40, "carbs": 22, "fat": 25},

    {"name": "Sinh tố chuối whey", "calories": 320, "protein": 30, "carbs": 35, "fat": 5},
    {"name": "Smoothie xoài hạt chia", "calories": 290, "protein": 8, "carbs": 40, "fat": 10},

    {"name": "Trứng ốp la bánh mì nguyên cám", "calories": 400, "protein": 22, "carbs": 35, "fat": 20},

    {"name": "Ức gà sốt teriyaki gạo lứt", "calories": 500, "protein": 40, "carbs": 60, "fat": 8},
    {"name": "Ức gà sốt tiêu đen bông cải", "calories": 420, "protein": 45, "carbs": 20, "fat": 12},

    {"name": "Yến mạch chuối sữa", "calories": 370, "protein": 15, "carbs": 55, "fat": 10},
    {"name": "Pancake yến mạch", "calories": 390, "protein": 18, "carbs": 50, "fat": 12},

    {"name": "Bowl đậu hũ nướng rau củ", "calories": 420, "protein": 25, "carbs": 50, "fat": 15},
    {"name": "Bowl gạo lứt cá hồi", "calories": 550, "protein": 38, "carbs": 55, "fat": 22},
    {"name": "Bowl gạo lứt ức gà", "calories": 500, "protein": 42, "carbs": 58, "fat": 8},
    {"name": "Bowl quinoa trứng luộc", "calories": 480, "protein": 25, "carbs": 55, "fat": 18},

    {"name": "Cá basa hấp khoai lang", "calories": 420, "protein": 35, "carbs": 45, "fat": 6},
    {"name": "Cá hồi áp chảo", "calories": 520, "protein": 40, "carbs": 10, "fat": 35},
]
if st.button("Phân tích"):

    status = st.empty()

    status.info("🔬 Đang phân tích chỉ số sinh học...")
    time.sleep(0.7)

    status.info("🧬 Đang đánh giá mức độ stress & thiếu ngủ...")
    time.sleep(0.7)

    status.info("📊 Tối ưu hóa thực đơn cá nhân hóa...")
    time.sleep(0.7)

    tdee = calculate_tdee(weight, height, age, gender, activity_level)

    status.success("✅ Phân tích hoàn tất!")
    st.metric("TDEE của bạn", int(tdee))
    if goal == "Giảm cân":
        target_calories = tdee - 400
    elif goal == "Tăng cân":
        target_calories = tdee + 300
    else:
        target_calories = tdee

    st.info(f"🎯 Mục tiêu năng lượng: {int(target_calories)} kcal/ngày")

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

    if activity_level == "Vận động nhiều":
        personal_factor += 5

    impact_score += personal_factor
    # ===== NEURO BALANCE INDEX =====

    stress_numeric = stress_value  # em đã có stress_value phía trên

    neuro_score = (
        sleep_score * 0.4 +
        (100 - stress_numeric) * 0.4 +
        (impact_score) * 0.2
    )

    st.subheader("🧠 Neuro Balance Index")
    st.metric("Neuro Score", round(neuro_score, 1))
    st.info("""
    🧠 Neuro Balance Index là chỉ số tổng hợp phản ánh mức độ cân bằng của hệ thần kinh dựa trên:
    - Giấc ngủ (khả năng phục hồi não)
    - Mức độ stress (căng thẳng nội tiết)
    - Mức vận động (kích hoạt sinh học)

Điểm cao = Hệ thần kinh đang ổn định  
Điểm thấp = Có nguy cơ mất cân bằng hoặc kiệt sức
""")
    # ===== PHÂN LOẠI RỦI RO =====
    if neuro_score >= 80:
        neuro_state = "Tối ưu"
    elif neuro_score >= 60:
        neuro_state = "Mất cân bằng nhẹ"
    elif neuro_score >= 40:
        neuro_state = "Nguy cơ Burnout"
    else:
        neuro_state = "Suy giảm thần kinh cao"

    st.write(f"**Phân loại:** {neuro_state}")
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
    st.subheader("📊 Hồ sơ sức khỏe cá nhân")

    col1, col2, col3 = st.columns(3)

    col1.metric("BMI", round(bmi,1))
    col2.metric("Sleep Score", sleep_score)
    col3.metric("Impact Score", round(impact_score,1))
    st.caption(f"AI đã điều chỉnh phân tích dựa trên mục tiêu '{goal}' và mức vận động '{activity_level}'.")

    if impact_score > 70:
        st.error("🔴 Tình trạng đáng lo ngại – Cần cải thiện giấc ngủ và giảm stress ngay.")
    elif impact_score > 40:
        st.warning("🟡 Có dấu hiệu ảnh hưởng đến hiệu suất học tập.")
    else:
        st.success("🟢 Ổn định – Tác động thấp đến sức khỏe tinh thần.")

    st.write(f"**Phân tích stress:** {stress_status}")
    # ===== DỰ BÁO 5 NGÀY =====

    burnout_risk = 100 - neuro_score

    future_scores = []
    future_score = neuro_score

    for i in range(5):
        future_score -= burnout_risk * 0.05
        future_scores.append(max(future_score, 0))

    import pandas as pd

    df = pd.DataFrame({
        "Ngày": ["1", "2", "3", "4", "5"],
        "Neuro Score dự báo": future_scores
    })

    st.subheader("📉 Dự báo xu hướng 5 ngày")
    st.line_chart(df.set_index("Ngày"))
    fig2, ax2 = plt.subplots()
    ax2.plot(df["Ngày"], df["Neuro Score dự báo"], marker='o')
    ax2.set_ylabel("Neuro Score")
    ax2.set_ylim(0, 100)
    ax2.set_title("Dự báo xu hướng 5 ngày")

    st.pyplot(fig2)
    # ===== AI ACTION PLAN =====

    st.subheader("🚀 Kế hoạch cải thiện")

    actions = []

    if sleep < 6:
        actions.append("Ngủ tối thiểu 7.5 giờ trong 3 ngày tới.")

    if stress_value > 60:
        actions.append("Thực hành hít thở sâu 10 phút mỗi ngày.")

    if bmi > 23:
        actions.append("Giảm 300 kcal/ngày và tăng 20 phút vận động.")

    if not actions:
        st.success("Trạng thái ổn định. Duy trì lối sống hiện tại.")
    else:
        for act in actions:
            st.write("- " + act)

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

       

        

    st.subheader("🥗 Đề xuất dinh dưỡng phục hồi")
    st.divider()
    def calculate_final_score(item, sleep_score, stress_value, goal, bmi):
      score = 0

      # Ưu tiên protein cao
      score += min(item["protein"], 40) * 0.7

      # Nếu goal là giảm cân → ưu tiên ít carb, ít fat
      if goal == "Giảm cân":
         score += max(0, 60 - item["carbs"]) * 0.3
         score += max(0, 25 - item["fat"]) * 0.5

      # Nếu goal tăng cơ → ưu tiên protein cao
      elif goal == "Tăng cơ":
         score += item["protein"] * 0.8

      # Nếu goal tăng năng lượng → ưu tiên carb cao
      elif goal == "Tăng năng lượng":
         score += item["carbs"] * 0.5

      # Stress cao → ưu tiên ít fat nặng
      if stress_value > 60:
         score += max(0, 30 - item["fat"])

      # BMI cao → trừ điểm món quá nhiều calo
      if bmi > 23:
         score -= max(0, item["calories"] - 500) * 0.2

      return score


    recommended = []

    for item in foods:

        if allergies and "contains" in item:
           if any(allergy in item["contains"] for allergy in allergies):
              continue

        score = calculate_final_score(
            item,
            sleep_score,
            stress_value,
            goal,
            bmi
        )

        recommended.append((item, score))

    recommended.sort(key=lambda x: x[1], reverse=True)

    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    images = os.path.join(BASE_DIR, "images")

    st.subheader("🏆 Top 3 món phù hợp nhất:")

    if len(recommended) > 0:

        for item, score in recommended[:3]:

            image_path = os.path.join(
                images,
                f"{normalize_name(item['name'])}.jpg"
            )

            col_img, col_info = st.columns([1, 2])

            with col_img:
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.warning(f"Không tìm thấy ảnh: {image_path}")

            with col_info:
                st.markdown(f"### 🍽 {item['name']}")
                st.write(f"🔥 {item['calories']} kcal")
                st.write(f"💪 {item['protein']}g protein")
                st.write(f"🍞 {item['carbs']}g carbs")
                st.write(f"🥑 {item['fat']}g fat")

            st.divider()

if st.button("📅 Tạo kế hoạch dinh dưỡng 7 ngày cá nhân hóa"):
    
    with st.spinner("AI đang phân tích sinh học của bạn..."):
      time.sleep(1.5)
    # ===== TÍNH TDEE =====
    tdee = calculate_tdee(weight, height, age, gender, activity_level)

    if goal == "Giảm cân":
        target_calories = tdee - 400
    elif goal == "Tăng cân":
        target_calories = tdee + 300
    else:
        target_calories = tdee

    st.info(f"🎯 Mục tiêu năng lượng: {int(target_calories)} kcal/ngày")

    # ===== TẠO KẾ HOẠCH 7 NGÀY =====
    import random

    weekly_plan = []

    for day in range(7):

        daily_meals = []
        total_day_calories = 0
        total_day_protein = 0

        while total_day_calories < target_calories * 0.95:
            item = random.choice(foods)

            daily_meals.append(item)
            total_day_calories += item["calories"]
            total_day_protein += item["protein"]

        weekly_plan.append({
            "day": day + 1,
            "meals": daily_meals,
            "calories": total_day_calories,
            "protein": total_day_protein
        })

    # ===== HIỂN THỊ =====
    st.subheader("📅 Kế hoạch dinh dưỡng 7 ngày")

    for day_data in weekly_plan:

        st.markdown(f"## 📅 Ngày {day_data['day']}")

        for i, meal in enumerate(day_data["meals"]):

            with st.expander(f"🍽 Bữa {i+1} - {meal['name']}"):

                image_path = os.path.join(
                    images,
                    f"{normalize_name(meal['name'])}.jpg"
                )

                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)

                st.write(f"🔥 {meal['calories']} kcal")
                st.write(f"💪 {meal['protein']}g protein")
                st.write(f"🍞 {meal['carbs']}g carbs")
                st.write(f"🥑 {meal['fat']}g fat")

        st.markdown(
            f"### 🔥 Tổng ngày: {int(day_data['calories'])} kcal | 💪 {int(day_data['protein'])}g protein"
        )

        st.divider()
        st.progress(min(day_data["calories"] / target_calories, 1.0))
    # ===== TỔNG 7 NGÀY =====
    total_calories = sum(day["calories"] for day in weekly_plan)
    total_protein = sum(day["protein"] for day in weekly_plan)

    st.subheader("📊 Tổng dinh dưỡng 7 ngày")

    colA, colB = st.columns(2)
    colA.metric("🔥 Tổng Calories", f"{int(total_calories)} kcal")
    colB.metric("💪 Tổng Protein", f"{int(total_protein)} g")
    st.markdown("### 🧬 Cơ sở khoa học")

    st.info("""
    - Thiếu ngủ làm tăng cortisol → ảnh hưởng chuyển hóa năng lượng  
    - Stress cao gây rối loạn glucose  
    - BMI cao liên quan nguy cơ chuyển hóa  
    - Protein giúp ổn định đường huyết và tăng no lâu  
    """)