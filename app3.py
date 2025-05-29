import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import torch
from torchvision import models, transforms
import torchvision

# โหลดโมเดล Faster R-CNN pretrained สำหรับ object detection
@st.cache_resource
def load_model():
    model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    return model

model = load_model()

# label ของ COCO dataset (80 class)
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella',
    'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
    'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass', 'cup', 'fork',
    'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'N/A', 'dining table', 'N/A', 'N/A', 'toilet',
    'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# ฟังก์ชันแปลงภาพและทำ object detection
def predict(image):
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    img = transform(image)
    with torch.no_grad():
        predictions = model([img])
    return predictions[0]

st.title("Object Detection with Streamlit")

# เลือก input
option = st.radio("เลือกวิธีโหลดรูปภาพ", ("จาก URL", "อัปโหลดไฟล์"))

img = None
if option == "จาก URL":
    url = st.text_input("กรุณาใส่ URL รูปภาพ")
    if url:
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            st.image(img, caption="รูปภาพที่โหลดจาก URL", use_container_width =True)
        except:
            st.error("โหลดรูปภาพไม่สำเร็จ โปรดตรวจสอบ URL อีกครั้ง")
elif option == "อัปโหลดไฟล์":
    uploaded_file = st.file_uploader("เลือกไฟล์รูปภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="รูปภาพที่อัปโหลด", use_container_width =True)

# ถ้ามีรูปภาพ ให้ตรวจจับวัตถุ
if img:
    st.write("กำลังวิเคราะห์รูปภาพ...")
    preds = predict(img)

    # เลือก object ที่มีความมั่นใจมากกว่า 0.5
    threshold = 0.5
    pred_classes = [COCO_INSTANCE_CATEGORY_NAMES[i] for i, score in zip(preds['labels'], preds['scores']) if score > threshold]
    pred_scores = [score.item() for score in preds['scores'] if score > threshold]

    if pred_classes:
        st.write("วัตถุที่พบในภาพ:")
        for cls, score in zip(pred_classes, pred_scores):
            st.write(f"- {cls} (ความมั่นใจ: {score:.2f})")
    else:
        st.write("ไม่พบวัตถุที่มีความมั่นใจสูงพอในภาพนี้")
