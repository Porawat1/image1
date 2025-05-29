import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.set_page_config(layout="wide")
st.title("📸 ระบบดูภาพ")

image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/British_shorthair_with_calico_coat_%282%29.jpg/330px-British_shorthair_with_calico_coat_%282%29.jpg",
    "เสือ": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Panthera_tigris_altaica_female.jpg/500px-Panthera_tigris_altaica_female.jpg"
}

headers = {
    "User-Agent": "MyStreamlitApp/1.0 (example@example.com)"
}

# Session state setup
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

def add_axes_to_image(img, width, height, spacing=100):
    """เพิ่มแกน X และ Y พร้อมตัวเลขรอบภาพ"""
    img = img.resize((width, height))
    font_size = 16
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    margin_x = 50
    margin_y = 50

    canvas = Image.new("RGB", (width + margin_x, height + margin_y), "white")
    canvas.paste(img, (margin_x, 0))
    draw = ImageDraw.Draw(canvas)

    # แกน Y (ซ้าย)
    for y in range(0, height + 1, spacing):
        draw.line([(margin_x - 5, y), (margin_x, y)], fill="black")
        draw.text((0, y - 7), str(y), fill="black", font=font)

    # แกน X (ล่าง)
    for x in range(0, width + 1, spacing):
        draw.line([(margin_x + x, height), (margin_x + x, height + 5)], fill="black")
        draw.text((margin_x + x - 10, height + 10), str(x), fill="black", font=font)

    return canvas

def blend_images(base_img, overlay_img, alpha):
    """ซ้อน overlay_img ลงบน base_img ด้วย alpha"""
    overlay_resized = overlay_img.resize(base_img.size).convert("RGBA")
    base_img_rgba = base_img.convert("RGBA")
    blended = Image.blend(base_img_rgba, overlay_resized, alpha)
    return blended.convert("RGB")

def show_thumbnail_page():
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
    name = st.session_state.selected_image
    url = image_urls.get(name)

    if not url:
        st.error("ไม่พบ URL ของรูปภาพนี้")
        return

    base_img = load_image_cached(url)
    if base_img:
        st.markdown(f"### ดูภาพขนาดใหญ่: **{name}**")
        left_col, right_col = st.columns([1.2, 3])

        with left_col:
            st.subheader("🔧 ปรับขนาดและความชัด")
            width = st.slider("ความกว้าง (px)", 100, 1200, 700, 50)
            height = st.slider("ความสูง (px)", 100, 1200, 500, 50)

            st.markdown("### 🔍 ความชัดของภาพรอง")
            overlay_opacity = {}
            for other_name in image_urls:
                if other_name != name:
                    overlay_opacity[other_name] = st.slider(
                        f"ความชัด '{other_name}'", 0.0, 1.0, 0.0, 0.05)

            st.markdown("---")
            if st.button("🔙 กลับไปหน้าเลือกภาพ"):
                st.session_state.selected_image = None

        # Resize และรวมภาพรองตามความชัด
        main_resized = base_img.resize((width, height)).convert("RGB")
        blended_img = main_resized

        for other_name, opacity in overlay_opacity.items():
            if opacity > 0:
                other_img = load_image_cached(image_urls[other_name])
                if other_img:
                    blended_img = blend_images(blended_img, other_img, opacity)

        final_img_with_axes = add_axes_to_image(blended_img, width, height)
        with right_col:
            st.image(final_img_with_axes, caption=f"{name} + ภาพซ้อน พร้อมแกน X/Y", use_column_width=False)

# Main logic
if st.session_state.selected_image is None:
    show_thumbnail_page()
else:
    show_full_image_page()
