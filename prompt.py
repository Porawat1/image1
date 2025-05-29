import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(layout="wide")
st.title("📸 ระบบดูภาพแบบเลือกแล้วแสดงเต็มจอ")

image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/British_shorthair_with_calico_coat_%282%29.jpg/330px-British_shorthair_with_calico_coat_%282%29.jpg",
    "เสือ": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Panthera_tigris_altaica_female.jpg/500px-Panthera_tigris_altaica_female.jpg"
}

headers = {
    "User-Agent": "MyStreamlitApp/1.0 (example@example.com)"
}

# Initial session_state setup
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None
if "cached_images" not in st.session_state:
    st.session_state.cached_images = {}

def load_image_cached(url):
    if url in st.session_state.cached_images:
        return st.session_state.cached_images[url]
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        st.session_state.cached_images[url] = img
        return img
    except Exception as e:
        st.error(f"โหลดรูปภาพไม่สำเร็จ: {e}")
        return None

def show_thumbnail_page():
    st.write("### เลือกรูปภาพที่คุณต้องการดูแบบขยาย")
    cols = st.columns(len(image_urls))
    for col, (name, url) in zip(cols, image_urls.items()):
        img = load_image_cached(url)
        if img:
            with col:
                st.image(img, caption=name, width=150)
                if st.button(f"ดู {name}", key=f"btn_{name}"):
                    st.session_state.selected_image = name

def show_full_image_page():
    name = st.session_state.selected_image
    st.write(f"### รูปภาพขนาดใหญ่: {name}")
    url = image_urls.get(name)
    if not url:
        st.error("ไม่พบ URL ของรูปภาพนี้")
        return

    img = load_image_cached(url)
    if img:
        left_col, right_col = st.columns([1, 3])
        with left_col:
            width = st.slider("ปรับความกว้างภาพ (px)", min_value=100, max_value=1200, value=700, step=10)
            height = st.slider("ปรับความสูงภาพ (px)", min_value=100, max_value=1200, value=500, step=10)
            if st.button("กลับไปหน้าเลือกภาพ"):
                st.session_state.selected_image = None
        
        with right_col:
            resized_img = img.resize((width, height))
            st.image(resized_img, caption=name, use_column_width=True)

# Main logic
if st.session_state.selected_image is None:
    show_thumbnail_page()
else:
    show_full_image_page()
