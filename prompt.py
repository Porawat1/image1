import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(layout="wide")
st.title("ระบบดูภาพแบบเลือกแล้วแสดงเต็มจอ")

image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/British_shorthair_with_calico_coat_%282%29.jpg/330px-British_shorthair_with_calico_coat_%282%29.jpg",
    "เสือ": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Panthera_tigris_altaica_female.jpg/500px-Panthera_tigris_altaica_female.jpg"
}

headers = {
    "User-Agent": "MyStreamlitApp/1.0 (example@example.com)"
}

# ถ้า session_state ไม่มี selected_image ให้เซ็ตเป็น None
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

def show_thumbnail_page():
    st.write("### เลือกรูปภาพที่คุณต้องการดูแบบขยาย")
    cols = st.columns(len(image_urls))
    for i, (name, url) in enumerate(image_urls.items()):
        with cols[i]:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                st.image(img, caption=name, width=150)
                if st.button(f"ดู {name}", key=f"btn_{name}"):
                    st.session_state.selected_image = name
                    st.experimental_rerun()
            except Exception as e:
                st.error(f"โหลดรูป {name} ไม่ได้: {e}")

def show_full_image_page():
    name = st.session_state.selected_image
    st.write(f"### รูปภาพขนาดใหญ่: {name}")
    url = image_urls[name]
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=name, use_column_width=True)
    except Exception as e:
        st.error(f"ไม่สามารถโหลดรูปภาพขนาดใหญ่ได้: {e}")

    if st.button("กลับไปหน้าเลือกภาพ"):
        st.session_state.selected_image = None
        st.experimental_rerun()

# แสดงหน้าเลือกภาพ หรือหน้าแสดงภาพใหญ่ ตามสถานะ selected_image
if st.session_state.selected_image is None:
    show_thumbnail_page()
else:
    show_full_image_page()
