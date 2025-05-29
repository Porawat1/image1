import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(layout="wide")
st.title("เลือกรูปภาพที่คุณต้องการดูแบบขยาย")

# URLs ของรูปภาพ
image_urls = {
    "บูลด็อก": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมว": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/British_shorthair_with_calico_coat_%282%29.jpg/330px-British_shorthair_with_calico_coat_%282%29.jpg",
    "เสือ": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Panthera_tigris_altaica_female.jpg/500px-Panthera_tigris_altaica_female.jpg"
}

# Header สำหรับหลีกเลี่ยง 403
headers = {
    "User-Agent": "MyStreamlitApp/1.0 (example@example.com)"
}

# เก็บสถานะใน session
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

# แสดงรูป thumbnail แบบขนาดเล็กในคอลัมน์
cols = st.columns(len(image_urls))

for i, (name, url) in enumerate(image_urls.items()):
    with cols[i]:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=name, width=150)  # 👈 ทำให้ thumbnail เล็กลง
            if st.button(f"ดู {name}", key=f"btn_{name}"):
                st.session_state.selected_image = name
        except Exception as e:
            st.error(f"โหลดรูป {name} ไม่ได้: {e}")

# แสดง "ป๊อปอัปจำลอง" ถ้าเลือกภาพ
if st.session_state.selected_image:
    st.markdown(
        """
        <style>
        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .popup-image {
            max-width: 90%;
            max-height: 90%;
            border: 5px solid white;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    big_url = image_urls[st.session_state.selected_image]
    try:
        response = requests.get(big_url, headers=headers)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_data = buffered.getvalue()
        img_base64 = f"data:image/jpeg;base64,{img_data.hex()}"

        # แสดง overlay ด้วย HTML
        st.markdown(
            f"""
            <div class="overlay" onclick="window.location.reload();">
                <img src="data:image/jpeg;base64,{img_data.hex()}" class="popup-image" />
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"ไม่สามารถโหลดรูปภาพขนาดใหญ่ได้: {e}")
