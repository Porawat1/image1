import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# หัวข้อหลัก
st.title("เลือกรูปภาพเพื่อแสดง")

# URLs ของรูปภาพ (ใช้ลิงก์ใหม่ที่โหลดได้แน่นอน)
image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "ไซบีเรียน ฮัสกี้": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Siberian_Husky_puppy.jpg",
    "โกลเด้น รีทรีฟเวอร์": "https://upload.wikimedia.org/wikipedia/commons/7/74/Golden_Retriever_Carlos_%2810541340993%29.jpg"
}

# แสดงตัวเลือกภาพ
choice = st.radio("เลือกรูปภาพที่คุณต้องการดู:", list(image_urls.keys()))

# ดึงรูปภาพจาก URL ที่เลือก
selected_url = image_urls[choice]
response = requests.get(selected_url)

# แสดงภาพที่เลือก
if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    st.image(img, caption=choice, use_column_width=True)
