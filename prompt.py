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

# สร้างคอลัมน์ 3 ช่องสำหรับรูปภาพย่อ
cols = st.columns(3)
selected = None

for idx, (label, url) in enumerate(image_urls.items()):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            with cols[idx]:
                st.image(img, caption=label, use_column_width=True)
                if st.button(f"เลือก {label}"):
                    selected = (label, img)
        else:
            st.warning(f"โหลดรูป {label} ไม่สำเร็จ")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดกับ {label}: {e}")

# แสดงภาพใหญ่ที่เลือก
if selected:
    st.markdown("---")
    st.subheader(f"คุณเลือกรูป: {selected[0]}")
    st.image(selected[1], caption=selected[0], use_column_width=True)
