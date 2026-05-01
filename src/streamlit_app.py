# ...existing code from streamlit_app.py...
import streamlit as st
import requests
from PIL import Image, ImageDraw
import io

# مهم في Docker
API_URL = "http://api:8000"

# 🎨 إعداد الصفحة
st.set_page_config(
    page_title="Car Parking Detection",
    page_icon="🚗",
    layout="wide"
)

# 🎨 CSS بسيط يخلي الشكل professional
st.markdown("""
    <style>
    .metric-card {
        background-color: #111;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .title {
        font-size: 28px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 🧭 Sidebar
st.sidebar.title("⚙️ Controls")
uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "png"])
detect_btn = st.sidebar.button("🚀 Run Detection")

# 🏷 Title
st.markdown('<p class="title">🚗 Car Parking Detection Dashboard</p>', unsafe_allow_html=True)

# Layout columns
col1, col2 = st.columns([2, 1])

if uploaded_file:

    image = Image.open(uploaded_file)

    if detect_btn:
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_URL}/predict", files=files)

        if response.status_code == 200:
            data = response.json()
            detections = data["detections"]

            # 🟥 رسم bounding boxes
            draw = ImageDraw.Draw(image)
            for det in detections:
                x1, y1, x2, y2 = det["bbox"]
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

            # 📊 عرض الصورة
            with col1:
                st.image(image, caption="Detection Result", use_column_width=True)

            # 📈 Stats
            with col2:
                st.subheader("📊 Statistics")

                total = len(detections)
                st.metric("🚗 Cars Detected", total)

                # لو عندك class للـ empty
                empty = sum(1 for d in detections if d["class"] == 0)
                occupied = total - empty

                st.metric("🅿️ Occupied", occupied)
                st.metric("🟢 Available", empty)

            # 📋 جدول
            st.subheader("📋 Detection Details")
            st.dataframe(detections)

        else:
            st.error("❌ API Error")
    else:
        st.image(image, caption="Uploaded Image", use_column_width=True)

else:
    st.info("👈 Upload an image from sidebar")