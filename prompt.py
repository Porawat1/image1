import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("เลือกรูปภาพที่คุณต้องการดูแบบขยาย")

# URLs ของรูปภาพ
image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "เเมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/British_shorthair_with_calico_coat_%282%29.jpg/330px-British_shorthair_with_calico_coat_%282%29.jpg",
    "เสือ": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Panthera_tigris_altaica_female.jpg/500px-Panthera_tigris_altaica_female.jpg"
}

# เพิ่ม headers สำหรับ Wikimedia
headers = {
    "User-Agent": "MyStreamlitApp/1.0 (example@example.com)"
}

# สร้าง layout เป็นคอลัมน์แนวนอน
cols = st.columns(len(image_urls))

# ตัวแปรเก็บค่ารูปที่เลือก
selected_image_key = None

# แสดงรูปภาพแบบ thumbnail พร้อมปุ่ม
for i, (name, url) in enumerate(image_urls.items()):
    with cols[i]:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=name, use_column_width=True)
            if st.button(f"ดู {name}", key=name):
                selected_image_key = name
        except Exception as e:
            st.error(f"โหลดรูป {name} ไม่ได้: {e}")

# ถ้ามีการเลือกภาพใด ๆ
if selected_image_key:
    st.markdown("---")
    st.subheader(f"รูปที่คุณเลือก: {selected_image_key}")
    try:
        big_url = image_urls[selected_image_key]
        response = requests.get(big_url, headers=headers)
        response.raise_for_status()
        big_img = Image.open(BytesIO(response.content))
        st.image(big_img, caption=selected_image_key, use_column_width=True)
    except Exception as e:
        st.error(f"ไม่สามารถโหลดรูปภาพขนาดใหญ่ได้: {e}")
