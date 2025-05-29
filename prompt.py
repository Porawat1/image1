import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.set_page_config(layout="wide")
st.title("📸 ระบบดูภาพและอัปโหลดภาพใหม่")

# ---------------------
# ส่วนของภาพเริ่มต้น
# ---------------------
default_images = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/British_shorthair_with_calico_coat_%282%29.jpg/330px-British_shorthair_with_calico_coat_%282%29.jpg",
    "เสือ": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Panthera_tigris_altaica_female.jpg/500px-Panthera_tigris_altaica_female.jpg"
}

headers = {"User-Agent": "MyStreamlitApp/1.0"}

# Session state setup
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None
if "cached_images" not in st.session_state:
    st.session_state.cached_images = {}
if "custom_images" not in st.session_state:
    st.session_state.custom_images = {}

# ---------------------
# ฟังก์ชันจัดการภาพ
# ---------------------
def load_image_from_url(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        st.error(f"โหลดภาพไม่สำเร็จจาก URL: {e}")
        return None

def load_image_cached(url):
    if url in st.session_state.cached_images:
        return st.session_state.cached_images[url]
    img = load_image_from_url(url)
    if img:
        st.session_state.cached_images[url] = img
    return img

def add_axes_to_image(img, width, height, spacing=100):
    img = img.resize((width, height))
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()

    margin_x, margin_y = 50, 50
    canvas = Image.new("RGB", (width + margin_x, height + margin_y), "white")
    canvas.paste(img, (margin_x, 0))
    draw = ImageDraw.Draw(canvas)

    for y in range(0, height + 1, spacing):
        draw.line([(margin_x - 5, y), (margin_x, y)], fill="black")
        draw.text((0, y - 7), str(y), fill="black", font=font)

    for x in range(0, width + 1, spacing):
        draw.line([(margin_x + x, height), (margin_x + x, height + 5)], fill="black")
        draw.text((margin_x + x - 10, height + 10), str(x), fill="black", font=font)

    return canvas

def blend_images(base_img, overlay_img, alpha):
    overlay_resized = overlay_img.resize(base_img.size).convert("RGBA")
    base_img_rgba = base_img.convert("RGBA")
    blended = Image.blend(base_img_rgba, overlay_resized, alpha)
    return blended.convert("RGB")

# ---------------------
# แสดงหน้าเลือกภาพ
# ---------------------
def show_thumbnail_page():
    st.markdown("### 🔍 เลือกหรืออัปโหลดภาพ")
    all_images = {**default_images, **st.session_state.custom_images}

    cols = st.columns(len(all_images))
    for col, (name, url_or_img) in zip(cols, all_images.items()):
        if isinstance(url_or_img, str):  # URL
            img = load_image_cached(url_or_img)
        else:  # Image object
            img = url_or_img

        if img:
            with col:
                st.image(img, caption=name, width=180)
                if st.button(f"ดู {name}", key=f"btn_{name}"):
                    st.session_state.selected_image = name
        else:
            with col:
                st.write(f"ไม่สามารถโหลดภาพ '{name}' ได้")

    st.markdown("---")
    st.subheader("🖼 เพิ่มภาพใหม่")
    col1, col2 = st.columns(2)

    with col1:
        uploaded = st.file_uploader("อัปโหลดภาพจากเครื่อง", type=["jpg", "jpeg", "png"])
        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            st.session_state.custom_images[uploaded.name] = img
            st.success(f"เพิ่มภาพ '{uploaded.name}' แล้ว")
            st.experimental_rerun()

    with col2:
        url = st.text_input("หรือป้อน URL ของภาพ")
        if url and st.button("โหลดภาพจาก URL"):
            img = load_image_from_url(url)
            if img:
                name = f"URL-{len(st.session_state.custom_images)+1}"
                st.session_state.custom_images[name] = img
                st.success(f"เพิ่มภาพจาก URL แล้วชื่อว่า '{name}'")
                st.experimental_rerun()

# ---------------------
# แสดงหน้าภาพขนาดใหญ่
# ---------------------
def show_full_image_page():
    all_images = {**default_images, **st.session_state.custom_images}
    name = st.session_state.selected_image
    selected_img = all_images.get(name)

    if not selected_img:
        st.error("ไม่พบภาพนี้")
        return

    st.markdown(f"### ดูภาพขนาดใหญ่: **{name}**")
    left_col, right_col = st.columns([1.2, 3])

    with left_col:
        st.subheader("🔧 ปรับขนาดและความชัด")
        width = st.slider("ความกว้าง (px)", 100, 1200, 700, 50)
        height = st.slider("ความสูง (px)", 100, 1200, 500, 50)

        overlay_opacity = {}
        for other_name, other_img in all_images.items():
            if other_name != name:
                overlay_opacity[other_name] = st.slider(
                    f"ความชัด '{other_name}'", 0.0, 1.0, 0.0, 0.05)

        st.markdown("---")
        if st.button("🔙 กลับไปหน้าเลือกภาพ"):
            st.session_state.selected_image = None
            st.experimental_rerun()

        st.subheader("🧠 (ตัวอย่าง) ตรวจจับวัตถุ")
        st.info("⚠️ คุณไม่ได้ติดตั้งโมเดลตรวจจับภาพ จึงแสดงข้อความจำลองเท่านั้น")
        st.write("🔹 จำลองผลลัพธ์: cat (0.99)")
        st.write("🔹 จำลองผลลัพธ์: dog (0.87)")

    base_resized = selected_img.resize((width, height)).convert("RGB")
    blended_img = base_resized

    for other_name, opacity in overlay_opacity.items():
        if opacity > 0:
            other_img = all_images[other_name]
            blended_img = blend_images(blended_img, other_img, opacity)

    final_img = add_axes_to_image(blended_img, width, height)

    with right_col:
        buf = BytesIO()
        final_img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.image(byte_im, caption=f"{name} + ภาพซ้อน พร้อมแกน X/Y", use_column_width=False)

# ---------------------
# Main app
# ---------------------
if st.session_state.selected_image is None:
    show_thumbnail_page()
else:
    show_full_image_page()
