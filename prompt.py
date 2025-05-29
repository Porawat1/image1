import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(layout="wide")
st.title("เลือกรูปภาพเพื่อแสดงขนาดใหญ่")

# URLs ของรูปภาพ
image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/British_shorthair_with_calico_coat_%282%29.jpg/330px-British_shorthair_with_calico_coat_%282%29.jpg",
    "เสือ": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Panthera_tigris_altaica_female.jpg/500px-Panthera_tigris_altaica_female.jpg"
}

# Header ป้องกัน 403
headers = {
    "User-Agent": "MyStreamlitApp/1.0 (example@example.com)"
}

# เก็บสถานะรูปที่เลือกใน session_state
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

# สร้างแถวของรูปเล็ก ๆ
cols = st.columns(len(image_urls))

for i, (name, url) in enumerate(image_urls.items()):
    with cols[i]:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=name, use_column_width=True)
            if st.button(f"🔍 ดู {name}", key=f"btn_{i}"):
                st.session_state.selected_image = name
        except Exception as e:
            st.error(f"โหลดรูป {name} ไม่ได้: {e}")

# ถ้ามีการเลือก ให้แสดง "ภาพใหญ่" ตรงกลาง
if st.session_state.selected_image:
    st.markdown("---")
    st.subheader(f"🔎 รูปภาพขนาดใหญ่: {st.session_state.selected_image}")
    big_url = image_urls[st.session_state.selected_image]
    try:
        response = requests.get(big_url, headers=headers)
        response.raise_for_status()
        big_img = Image.open(BytesIO(response.content))
        st.image(big_img, use_column_width=True)
        if st.button("❌ ปิดรูปภาพ"):
            st.session_state.selected_image = None
    except Exception as e:
        st.error(f"ไม่สามารถโหลดรูปภาพขนาดใหญ่ได้: {e}")
