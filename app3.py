import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import torch
from torchvision import models, transforms

@st.cache_resource
def load_model():
    model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    return model

model = load_model()

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

def predict(image):
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    img = transform(image)
    with torch.no_grad():
        predictions = model([img])
    return predictions[0]

def draw_boxes(image, boxes, labels, scores, threshold=0.5):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for box, label, score in zip(boxes, labels, scores):
        if score > threshold:
            xmin, ymin, xmax, ymax = box
            xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)

            # วาดกรอบสี่เหลี่ยม
            draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=3)
            # วาดข้อความ
            text = f"{label}: {score:.2f}"
            text_size = draw.textsize(text, font=font)
            # กล่องข้อความด้านหลังให้เห็นชัด
            draw.rectangle([xmin, ymin - text_size[1], xmin + text_size[0], ymin], fill="red")
            draw.text((xmin, ymin - text_size[1]), text, fill="white", font=font)
    return image

st.title("Object Detection with Streamlit")

option = st.radio("เลือกวิธีโหลดรูปภาพ", ("จาก URL", "อัปโหลดไฟล์"))

img = None
if option == "จาก URL":
    url = st.text_input("กรุณาใส่ URL รูปภาพ")
    if url:
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            st.image(img, caption="รูปภาพที่โหลดจาก URL", use_column_width=True)
        except:
            st.error("โหลดรูปภาพไม่สำเร็จ โปรดตรวจสอบ URL อีกครั้ง")
elif option == "อัปโหลดไฟล์":
    uploaded_file = st.file_uploader("เลือกไฟล์รูปภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="รูปภาพที่อัปโหลด", use_column_width=True)

if img:
    st.write("กำลังวิเคราะห์รูปภาพ...")
    preds = predict(img)

    boxes = preds['boxes'].tolist()
    labels = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in preds['labels'].tolist()]
    scores = preds['scores'].tolist()

    # วาดกรอบบนรูป
    img_with_boxes = img.copy()
    img_with_boxes = draw_boxes(img_with_boxes, boxes, labels, scores, threshold=0.5)

    st.image(img_with_boxes, caption="ผลลัพธ์พร้อมกรอบวัตถุ", use_column_width=True)

    # แสดงชื่อวัตถุที่ตรวจจับได้
    detected_objects = [label for label, score in zip(labels, scores) if score > 0.5]
    if detected_objects:
        st.write("วัตถุที่พบในภาพ:")
        for obj in set(detected_objects):
            st.write(f"- {obj}")
    else:
        st.write("ไม่พบวัตถุที่ชัดเจนในภาพ")
