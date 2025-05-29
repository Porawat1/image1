import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# หัวข้อของหน้าเว็บ
st.title("แสดงรูปภาพจาก URL")

# URL ของรูปภาพ
image_url = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg"

# ดึงข้อมูลรูปภาพจาก URL
response = requests.get(image_url)

# ตรวจสอบว่าโหลดรูปภาพสำเร็จหรือไม่
if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    st.image(img, caption="Bulldog Inglese", use_column_width=True)
else:
    st.error("ไม่สามารถโหลดรูปภาพจาก URL ได้")
