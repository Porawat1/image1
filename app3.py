from flask import Flask, request, render_template_string
from PIL import Image
import requests
from io import BytesIO
import torch
import torchvision.transforms as T

app = Flask(__name__)

# โหลดโมเดล Faster R-CNN ที่ผ่านการเทรนบน COCO dataset
model = torch.hub.load('pytorch/vision:v0.15.2', 'fasterrcnn_resnet50_fpn', pretrained=True)
model.eval()

# ชื่อวัตถุใน COCO dataset
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
    'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
    'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
    'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
    'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
    'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

def transform_image(image):
    transform = T.Compose([
        T.ToTensor(),
    ])
    return transform(image)

def get_objects(image):
    img_t = transform_image(image)
    with torch.no_grad():
        predictions = model([img_t])[0]

    threshold = 0.5  # confidence threshold
    labels = predictions['labels']
    scores = predictions['scores']

    detected_objects = set()
    for label, score in zip(labels, scores):
        if score > threshold:
            detected_objects.add(COCO_INSTANCE_CATEGORY_NAMES[label])

    return list(detected_objects)


# หน้าเว็บ
HTML_PAGE = '''
<!doctype html>
<title>Upload or Enter URL</title>
<h1>Upload an image or enter URL</h1>
<form method=post enctype=multipart/form-data>
  Upload Image: <input type=file name=file><br><br>
  Or enter Image URL: <input type=text name=url><br><br>
  <input type=submit value=Detect>
</form>
{% if objects %}
  <h2>Objects detected:</h2>
  <ul>
    {% for obj in objects %}
      <li>{{ obj }}</li>
    {% endfor %}
  </ul>
{% elif error %}
  <p style="color:red;">{{ error }}</p>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    objects = None
    error = None
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            # โหลดรูปจากไฟล์ที่อัปโหลด
            file = request.files['file']
            try:
                image = Image.open(file.stream).convert("RGB")
                objects = get_objects(image)
            except Exception as e:
                error = 'Error processing uploaded image.'
        elif request.form.get('url'):
            # โหลดรูปจาก URL
            url = request.form.get('url')
            try:
                response = requests.get(url)
                image = Image.open(BytesIO(response.content)).convert("RGB")
                objects = get_objects(image)
            except Exception as e:
                error = 'Error processing image from URL.'
        else:
            error = 'Please upload a file or enter an image URL.'
    return render_template_string(HTML_PAGE, objects=objects, error=error)

if __name__ == '__main__':
    app.run(debug=True)

