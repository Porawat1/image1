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

if "selected_image" not in st.session_state:
    st.session_state.selected_image = None
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def load_image(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.error(f"โหลดรูปภาพไม่สำเร็จ: {e}")
        return None

def show_thumbnail_page():
    st.write("### เลือกรูปภาพที่คุณต้องการดูแบบขยาย")
    cols = st.columns(len(image_urls))
    for i, (name, url) in enumerate(image_urls.items()):
        with cols[i]:
            img = load_image(url)
            if img:
                st.image(img, caption=name, width=150)
                if st.button(f"ดู {name}", key=f"btn_{name}"):
                    st.session_state.selected_image = name
                    st.session_state.button_clicked = True
                    # ไม่ต้องเรียก st.experimental_rerun() ตรงนี้

def show_full_image_page():
    name = st.session_state.selected_image
    st.write(f"### รูปภาพขนาดใหญ่: {name}")
    url = image_urls.get(name)
    if not url:
        st.error("ไม่พบ URL ของรูปภาพนี้")
        return

    img = load_image(url)
    if img:
        st.image(img, caption=name, use_column_width=True)

    if st.button("กลับไปหน้าเลือกภาพ"):
        st.session_state.selected_image = None
        st.session_state.button_clicked = False
        # ไม่ต้องเรียก st.experimental_rerun() ตรงนี้

# Main logic:
if st.session_state.selected_image is None:
    show_thumbnail_page()
else:
    show_full_image_page()

# หลังจาก render เสร็จแล้วถ้ากดปุ่ม ให้ rerun ทีหลัง
if st.session_state.button_clicked:
    st.session_state.button_clicked = False
    st.experimental_rerun()
