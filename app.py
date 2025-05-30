import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    decode_predictions,
    preprocess_input,
)
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# โหลดโมเดล MobileNetV2 ที่เทรนบน ImageNet
model = MobileNetV2(weights="imagenet")

st.title("Image Classification Application")
st.write("อัปโหลดภาพแล้วให้โมเดลทำนาย")

uploaded_file = st.file_uploader("เลือกภาพ...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # เปิดภาพและแปลงเป็น RGB
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Resize โดยใช้ TensorFlow
    image_resized = tf.image.resize(np.array(image), (224, 224))
    image_resized = image_resized.numpy().astype(np.uint8)

    # เตรียมข้อมูลภาพ
    img_array_expanded = np.expand_dims(image_resized, axis=0)
    processed_img = preprocess_input(img_array_expanded)

    # ทำนาย
    predictions = model.predict(processed_img)
    decoded_preds = decode_predictions(predictions, top=3)[0]

    st.write("### ผลการทำนาย:")
    for i, (imagenet_id, label, prob) in enumerate(decoded_preds):
        st.write(f"**{i+1}. {label}** ({prob*100:.2f}%)")
        st.progress(int(prob * 100))

    # Grad-CAM Visualization
    st.write("### Grad-CAM Visualization")

    # สร้างโมเดลย่อยเพื่อดึง feature map + output
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer("Conv_1").output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(processed_img)
        pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = np.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap) + 1e-8  # ป้องกันหารด้วย 0
    heatmap = heatmap.numpy()

    # Resize heatmap ให้เท่าขนาดภาพต้นฉบับ
    heatmap_resized = Image.fromarray(np.uint8(255 * heatmap)).resize(image.size)

    # ใส่ colormap
    colormap = cm.get_cmap("jet")
    colored_heatmap = colormap(np.array(heatmap_resized) / 255.0)
    colored_heatmap = (colored_heatmap[:, :, :3] * 255).astype(np.uint8)
    colored_heatmap_img = Image.fromarray(colored_heatmap)

    # ซ้อน heatmap กับภาพต้นฉบับ
    blended = Image.blend(image, colored_heatmap_img, alpha=0.4)

    st.image(blended, caption="Grad-CAM Heatmap", use_column_width=True)
