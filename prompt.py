import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("เลือกรูปภาพเพื่อแสดง")

# URLs ของรูปภาพ
image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "ไซบีเรียน ฮัสกี้": "https://upload.wikimedia.org/wikipedia/commons/6/60/Siberian_Husky_pho.jpg",
    "โกลเด้น รีทรีฟเวอร์": "https://upload.wikimedia.org/wikipedia/commons/0/08/Golden_retriever_eating_pigs_foot.jpg"
}

# สร้างคอลัมน์สำหรับแสดงภาพย่อด้านบน
cols = st.columns(3)
for idx, (label, url) in enumerate(image_urls.items()):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            with cols[idx]:
                st.image(img, caption=label, use_column_width=True)
        else:
            with cols[idx]:
                st.warning(f"โหลดรูป {label} ไม่สำเร็จ")
    except Exception as e:
        with cols[idx]:
            st.error(f"เกิดข้อผิดพลาดกับ {label}")

# ส่วนของตัวเลือกด้านล่าง
st.markdown("---")
choice = st.radio("เลือกรูปภาพที่คุณต้องการดูแบบใหญ่:", list(image_urls.keys()))

# แสดงภาพใหญ่ที่เลือก
try:
    selected_url = image_urls[choice]
    response = requests.get(selected_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=f"คุณเลือก: {choice}", use_column_width=True)
    else:
        st.error("ไม่สามารถโหลดรูปภาพจาก URL ได้")
except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
