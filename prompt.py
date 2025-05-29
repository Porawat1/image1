import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# หัวข้อหลัก
st.title("เลือกรูปภาพเพื่อแสดง")

# URLs ของรูปภาพ
image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "เเมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/British_shorthair_with_calico_coat_%282%29.jpg/330px-British_shorthair_with_calico_coat_%282%29.jpg",
    "เสือ": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Panthera_tigris_altaica_female.jpg/500px-Panthera_tigris_altaica_female.jpg"
}

# แสดงตัวเลือกภาพ
choice = st.radio("เลือกรูปภาพที่คุณต้องการดู:", list(image_urls.keys()))
selected_url = image_urls[choice]

# เพิ่ม headers สำหรับ Wikimedia
headers = {
    "User-Agent": "MyStreamlitApp/1.0 (example@example.com)"  # ใส่อะไรก็ได้ที่ดูเหมือน user-agent จริง
}

try:
    response = requests.get(selected_url, headers=headers)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    st.image(img, caption=choice, use_column_width=True)
except Exception as e:
    st.error(f"ไม่สามารถโหลดรูปภาพได้: {e}")
