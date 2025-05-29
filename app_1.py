
import streamlit as st
from skimage import io, color
from skimage.filters import threshold_otsu, sobel
from skimage.util import random_noise
from skimage.restoration import denoise_tv_chambolle
from skimage import exposure
from skimage.filters import unsharp_mask
from scipy.ndimage import gaussian_filter, median_filter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ตั้งชื่อแอป
st.title("Image Processing with scikit-image")

# โหลดภาพตัวอย่าง
image_urls = {
    "ภาพตัวอย่างที่ 1": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "ภาพตัวอย่างที่ 2": "https://vetmarlborough.co.nz/wp-content/uploads/old-cats.jpg"
}

# แสดงภาพตัวอย่างให้เลือก
st.subheader("เลือกรูปภาพที่ต้องการแปลง")
cols = st.columns(len(image_urls))

# ใช้ session_state เพื่อจำภาพที่เลือกไว้
if 'selected_image_url' not in st.session_state:
    st.session_state.selected_image_url = None

for i, (name, url) in enumerate(image_urls.items()):
    with cols[i]:
        st.image(url, caption=name, use_container_width=True)
        if st.button(f"เลือก {name}"):
            st.session_state.selected_image_url = url

selected_image_url = st.session_state.selected_image_url

# ถ้ามีการเลือกภาพ
if selected_image_url:
    # โหลดภาพ
    image = io.imread(selected_image_url)

    # ตรวจสอบว่าภาพมี 3 ช่องสี
    if image.ndim == 3 and image.shape[2] == 3:
        # ดึงช่อง R, G, B
        R = image[:, :, 0]
        G = image[:, :, 1]
        B = image[:, :, 2]

        st.subheader("ตารางค่าพิกเซลของภาพสี (R, G, B)")

        rgb_cols = st.columns(3)
        with rgb_cols[0]:
            st.markdown("#### ค่า R (แดง)")
            r_df = pd.DataFrame(R)
            st.dataframe(r_df)

        with rgb_cols[1]:
            st.markdown("#### ค่า G (เขียว)")
            g_df = pd.DataFrame(G)
            st.dataframe(g_df)

        with rgb_cols[2]:
            st.markdown("#### ค่า B (น้ำเงิน)")
            b_df = pd.DataFrame(B)
            st.dataframe(b_df)

    # แปลงเป็นภาพสีเทา
    gray_image = color.rgb2gray(image)

    # สร้างภาพขาวดำโดยใช้ threshold
    thresh = threshold_otsu(gray_image)
    binary_image = gray_image > thresh

    # สร้างภาพขอบ
    edge_image = sobel(gray_image)

    # แสดงผลลัพธ์
    st.subheader("ผลลัพธ์ที่ได้จากการแปลงภาพ")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ภาพสีเทา (Grayscale)")
        fig1, ax1 = plt.subplots()
        ax1.imshow(gray_image, cmap='gray')
        ax1.axis('off')
        st.pyplot(fig1)

        st.markdown("ตารางค่าพิกเซล (สีเทา) [0–155]")
        gray_scaled = (gray_image * 155).astype(int)
        gray_df = pd.DataFrame(gray_scaled)
        st.dataframe(gray_df)

    with col2:
        st.markdown("### ภาพขาวดำ (Binary)")
        fig2, ax2 = plt.subplots()
        ax2.imshow(binary_image, cmap='gray')
        ax2.axis('off')
        st.pyplot(fig2)

        st.markdown("ตารางค่าพิกเซล (ขาวดำ) [0 หรือ 1]")
        binary_int = binary_image.astype(int)
        binary_df = pd.DataFrame(binary_int)
        st.dataframe(binary_df)

    # แสดงภาพขอบ
    st.subheader("ภาพขอบ (Edge Image)")
    fig3, ax3 = plt.subplots()
    ax3.imshow(edge_image, cmap='gray')
    ax3.axis('off')
    st.pyplot(fig3)

    st.markdown("ตารางค่าพิกเซล (ขอบ) [ค่าความต่างของพิกเซล]")
    edge_df = pd.DataFrame(edge_image)
    st.dataframe(gray_df)

    # ปรับความสว่าง (Brightness Enhancement) - Grayscale
    st.subheader("Image Enhancement: ปรับความสว่างของภาพสีเทา")
    brightness_factor = st.slider("ปรับความสว่าง", -0.20, 0.20, 0.0, step=0.01)
    enhanced_gray = np.clip(gray_image + brightness_factor, 0, 1)

    st.subheader("ภาพสีเทาหลังปรับความสว่าง (Enhanced Gray Image)")
    fig4, ax4 = plt.subplots()
    ax4.imshow(enhanced_gray, cmap='gray')
    ax4.axis('off')
    st.pyplot(fig4)

    st.markdown("ตารางค่าพิกเซล (ภาพสีเทาหลังปรับ) [0–155]")
    enhanced_gray_scaled = (enhanced_gray * 155).astype(int)
    enhanced_gray_df = pd.DataFrame(enhanced_gray_scaled)
    st.dataframe(enhanced_gray_df)

    # ปรับความสว่างของภาพสี RGB
    st.subheader("Image Enhancement: ปรับความสว่างของภาพสี (RGB)")
    brightness_rgb = st.slider("ปรับความสว่างของภาพสี", -50, 50, 0, step=1)

    # ปรับค่าพิกเซลและจำกัดช่วง
    enhanced_rgb = image.astype(np.int16) + brightness_rgb
    enhanced_rgb = np.clip(enhanced_rgb, 0, 255).astype(np.uint8)

    st.subheader("ภาพสีหลังปรับความสว่าง (Enhanced RGB Image)")
    st.image(enhanced_rgb, use_container_width=True)

    st.subheader("ตารางค่าพิกเซลหลังปรับ (R, G, B) [0–255]")

    rgb_cols2 = st.columns(3)
    with rgb_cols2[0]:
        st.markdown("#### R (แดง)")
        r_enhanced = enhanced_rgb[:, :, 0]
        st.dataframe(pd.DataFrame(r_enhanced))

    with rgb_cols2[1]:
        st.markdown("#### G (เขียว)")
        g_enhanced = enhanced_rgb[:, :, 1]
        st.dataframe(pd.DataFrame(g_enhanced))

    with rgb_cols2[2]:
        st.markdown("#### B (น้ำเงิน)")
        b_enhanced = enhanced_rgb[:, :, 2]
        st.dataframe(pd.DataFrame(b_enhanced))

    # =============================
    # Image Processing: Adding Noise
    # =============================
    st.subheader("Image Processing: การเพิ่ม Noise ให้ภาพสี")

    noise_type = st.selectbox("เลือกประเภท Noise", ["gaussian", "salt", "pepper", "s&p"])

    # สำหรับ gaussian เท่านั้นถึงใช้ค่า variance ได้
    if noise_type == "gaussian":
        var = st.slider("ความรุนแรงของ Gaussian Noise (variance)", 0.001, 0.1, 0.01, step=0.001)
        noisy_image = random_noise(enhanced_rgb, mode=noise_type, var=var)
    else:
        amount = st.slider("ระดับของ Noise", 0.01, 0.2, 0.05, step=0.01)
        noisy_image = random_noise(enhanced_rgb, mode=noise_type, amount=amount)

    # แปลงจาก float [0,1] เป็น uint8 [0,255]
    noisy_image_uint8 = (np.clip(noisy_image, 0, 1) * 255).astype(np.uint8)

    # แสดงภาพ
    st.subheader("ภาพหลังจากเพิ่ม Noise")
    st.image(noisy_image_uint8, use_container_width=True)


    # ===================================
    # Image Restoration: ฟื้นฟูภาพที่มี Noise
    # ===================================
    st.subheader("Image Restoration: ฟื้นฟูภาพจาก Noise")

    restoration_method = st.selectbox("เลือกวิธีการฟื้นฟูภาพ", ["Median Filter", "Gaussian Filter", "Total Variation (TV) Denoising"])

    # ฟังก์ชันฟื้นฟูภาพ RGB ทีละช่อง
    def restore_rgb(image, method):
        restored = np.zeros_like(image, dtype=np.float32)
        for c in range(3):
            channel = image[:, :, c]
            if method == "Median Filter":
                restored[:, :, c] = median_filter(channel, size=3)
            elif method == "Gaussian Filter":
                restored[:, :, c] = gaussian_filter(channel, sigma=1)
            elif method == "Total Variation (TV) Denoising":
                restored[:, :, c] = denoise_tv_chambolle(channel, weight=0.1)
        return np.clip(restored, 0, 1)

    # คืนภาพที่ฟื้นฟูแล้ว
    restored_image = restore_rgb(noisy_image, restoration_method)

    # แปลงเป็น uint8
    restored_image_uint8 = (restored_image * 255).astype(np.uint8)

    # แสดงภาพที่ผ่านการฟื้นฟู
    st.subheader("เปรียบเทียบภาพก่อนและหลังการฟื้นฟู")

    compare_cols = st.columns(2)

    with compare_cols[0]:
        st.markdown("#### ก่อนฟื้นฟู (Noisy Image)")
        st.image(noisy_image_uint8, use_container_width=True)

    with compare_cols[1]:
        st.markdown("#### หลังฟื้นฟู (Restored Image)")
        st.image(restored_image_uint8, use_container_width=True)

    # ===================================
    # Image Enhancement: Contrast Adjustment
    # ===================================
    st.subheader("Image Enhancement: ปรับความคมชัดของภาพสี (Contrast)")

    contrast_factor = st.slider("ปรับระดับความคมชัด (Contrast)", 0.5, 2.0, 1.0, step=0.1)

    # ฟังก์ชันปรับ contrast แบบ linear บนภาพ RGB
    def adjust_contrast(image, factor):
        image_float = image.astype(np.float32) / 255.0
        mean = np.mean(image_float, axis=(0, 1), keepdims=True)
        adjusted = (image_float - mean) * factor + mean
        adjusted = np.clip(adjusted, 0, 1)
        return (adjusted * 255).astype(np.uint8)

    # ปรับ contrast ภาพสี
    contrast_image = adjust_contrast(enhanced_rgb, contrast_factor)

    # แสดงผลภาพ
    st.subheader("ภาพหลังปรับความคมชัด (Contrast Enhanced)")
    st.image(contrast_image, use_container_width=True)


    # ===================================
    # แสดง Histogram ของภาพ RGB หลังปรับ Contrast
    # ===================================
    st.subheader("Histogram ของภาพหลังปรับความคมชัด (Contrast Enhanced)")

    # ดึงแต่ละช่องสี
    r_channel = contrast_image[:, :, 0].flatten()
    g_channel = contrast_image[:, :, 1].flatten()
    b_channel = contrast_image[:, :, 2].flatten()

    # วาดกราฟ histogram
    fig_hist, ax_hist = plt.subplots()
    ax_hist.hist(r_channel, bins=256, color='red', alpha=0.5, label='R')
    ax_hist.hist(g_channel, bins=256, color='green', alpha=0.5, label='G')
    ax_hist.hist(b_channel, bins=256, color='blue', alpha=0.5, label='B')
    ax_hist.set_title("Histogram of Pixel Values (R, G, B)")
    ax_hist.set_xlabel("Intensity")
    ax_hist.set_ylabel("Number of Pixel")
    ax_hist.legend()

    st.pyplot(fig_hist)

    # ===================================
    # Show RGB Histograms (in English)
    # ===================================
    st.subheader("Histogram by Color Channel (after Contrast Enhancement)")

    # Extract RGB channels
    r_channel = contrast_image[:, :, 0].flatten()
    g_channel = contrast_image[:, :, 1].flatten()
    b_channel = contrast_image[:, :, 2].flatten()

    # Create 3 columns for R, G, B histograms
    hist_cols = st.columns(3)

    # Red Channel
    with hist_cols[0]:
        st.markdown("#### Red Channel (R)")
        fig_r, ax_r = plt.subplots()
        ax_r.hist(r_channel, bins=256, color='red')
        ax_r.set_xlim([0, 255])
        ax_r.set_title("Histogram of Red Channel")
        ax_r.set_xlabel("Pixel Intensity")
        ax_r.set_ylabel("Pixel Count")
        st.pyplot(fig_r)

    # Green Channel
    with hist_cols[1]:
        st.markdown("#### Green Channel (G)")
        fig_g, ax_g = plt.subplots()
        ax_g.hist(g_channel, bins=256, color='green')
        ax_g.set_xlim([0, 255])
        ax_g.set_title("Histogram of Green Channel")
        ax_g.set_xlabel("Pixel Intensity")
        ax_g.set_ylabel("Pixel Count")
        st.pyplot(fig_g)

    # Blue Channel
    with hist_cols[2]:
        st.markdown("#### Blue Channel (B)")
        fig_b, ax_b = plt.subplots()
        ax_b.hist(b_channel, bins=256, color='blue')
        ax_b.set_xlim([0, 255])
        ax_b.set_title("Histogram of Blue Channel")
        ax_b.set_xlabel("Pixel Intensity")
        ax_b.set_ylabel("Pixel Count")
        st.pyplot(fig_b)


    # ===================================
    # Show RGB Line Graph (Intensity Distribution)
    # ===================================
    st.subheader("Line Graph by Color Channel (after Contrast Enhancement)")

    # Extract each channel
    r_channel = contrast_image[:, :, 0].flatten()
    g_channel = contrast_image[:, :, 1].flatten()
    b_channel = contrast_image[:, :, 2].flatten()

    # Calculate histogram counts manually
    r_counts, _ = np.histogram(r_channel, bins=256, range=(0, 255))
    g_counts, _ = np.histogram(g_channel, bins=256, range=(0, 255))
    b_counts, _ = np.histogram(b_channel, bins=256, range=(0, 255))
    x = np.arange(256)

    # Create 3 columns for line graphs
    line_cols = st.columns(3)

    # Red Line Graph
    with line_cols[0]:
        st.markdown("#### Red Channel (R)")
        fig_r, ax_r = plt.subplots()
        ax_r.plot(x, r_counts, color='red')
        ax_r.set_xlim([0, 255])
        ax_r.set_title("Line Graph of Red Channel")
        ax_r.set_xlabel("Pixel Intensity")
        ax_r.set_ylabel("Pixel Count")
        st.pyplot(fig_r)

    # Green Line Graph
    with line_cols[1]:
        st.markdown("#### Green Channel (G)")
        fig_g, ax_g = plt.subplots()
        ax_g.plot(x, g_counts, color='green')
        ax_g.set_xlim([0, 255])
        ax_g.set_title("Line Graph of Green Channel")
        ax_g.set_xlabel("Pixel Intensity")
        ax_g.set_ylabel("Pixel Count")
        st.pyplot(fig_g)

    # Blue Line Graph
    with line_cols[2]:
        st.markdown("#### Blue Channel (B)")
        fig_b, ax_b = plt.subplots()
        ax_b.plot(x, b_counts, color='blue')
        ax_b.set_xlim([0, 255])
        ax_b.set_title("Line Graph of Blue Channel")
        ax_b.set_xlabel("Pixel Intensity")
        ax_b.set_ylabel("Pixel Count")
        st.pyplot(fig_b)
