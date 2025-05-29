import streamlit as st
import requests
from PIL import Image, ImageDraw
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

# Setup session state variables
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None
if "cached_images" not in st.session_state:
    st.session_state.cached_images = {}

def load_image_cached(url):
    """โหลดภาพจาก URL และเก็บใน cache ของ session_state"""
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

def add_grid_to_image(img, grid_spacing=50, line_color=(255, 0, 0, 128)):
    """เพิ่มเส้นกริดแกน X และ Y ลงบนภาพ"""
    img_with_grid = img.convert("RGBA")
    draw = ImageDraw.Draw(img_with_grid)
    width, height = img_with_grid.size

    # วาดเส้นแนวตั้ง (แกน Y)
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=line_color, width=1)

    # วาดเส้นแนวนอน (แกน X)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=line_color, width=1)

    return img_with_grid

def show_thumbnail_page():
    """แสดงหน้ารายการภาพเล็กสำหรับเลือก"""
    st.markdown("### เลือกรูปภาพที่คุณต้องการดูแบบขยาย")
    cols = st.columns(len(image_urls))
    for col, (name, url) in zip(cols, image_urls.items()):
        img = load_image_cached(url)
        if img:
            with col:
                st.image(img, caption=name, width=180)
                if st.button(f"ดู {name}", key=f"btn_{name}"):
                    st.session_state.selected_image = name

def show_full_image_page():
    """แสดงภาพขนาดใหญ่พร้อม slider ปรับขนาดและปุ่มย้อนกลับ"""
    name = st.session_state.selected_image
    url = image_urls.get(name)

    if not url:
        st.error("ไม่พบ URL ของรูปภาพนี้")
        return

    img = load_image_cached(url)
    if img:
        st.markdown(f"### ดูภาพขนาดใหญ่: **{name}**")

        # แบ่งพื้นที่เป็น 2 คอลัมน์: ซ้ายสำหรับควบคุม, ขวาสำหรับแสดงภาพ
        left_col, right_col = st.columns([1, 3])

        with left_col:
            st.subheader("ปรับขนาดภาพ")
            width = st.slider("ความกว้าง (px)", min_value=100, max_value=1200, value=700, step=10)
            height = st.slider("ความสูง (px)", min_value=100, max_value=1200, value=500, step=10)
            st.markdown("---")
            if st.button("🔙 กลับไปหน้าเลือกภาพ"):
                st.session_state.selected_image = None

        with right_col:
            img_with_grid = add_grid_to_image(img)
            resized_img = img_with_grid.resize((width, height))
            st.image(resized_img, caption=name, use_container_width=False)

# Main app logic
if st.session_state.selected_image is None:
    show_thumbnail_page()
else:
    show_full_image_page()
