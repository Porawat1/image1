import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# หัวข้อหลัก
st.title("เลือกรูปภาพเพื่อแสดง")

# URLs ของรูปภาพ (ใช้ลิงก์ใหม่ที่โหลดได้แน่นอน)
image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "เเมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/British_shorthair_with_calico_coat_%282%29.jpg/330px-British_shorthair_with_calico_coat_%282%29.jpg",
    "เสือ": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Panthera_tigris_altaica_female.jpg/500px-Panthera_tigris_altaica_female.jpg"
}

# แสดงตัวเลือกภาพ
choice = st.radio("เลือกรูปภาพที่คุณต้องการดู:", list(image_urls.keys()))

# ดึงรูปภาพจาก URL ที่เลือก
selected_url = image_urls[choice]

try:
    response = requests.get(selected_url)
    response.raise_for_status()  # จะ throw error ถ้าสถานะไม่ใช่ 200
    img = Image.open(BytesIO(response.content))
    st.image(img, caption=choice, use_column_width=True)
except Exception as e:
    st.error(f"ไม่สามารถโหลดรูปภาพได้: {e}")
