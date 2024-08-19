from flask import Flask, request, jsonify
import torch
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.datasets import letterbox
from yolov5.utils.plots import plot_one_box
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load YOLOv5 model
model = attempt_load('yolov5/yolov5s.pt', map_location='cpu')

def preprocess_image(image):
    img = letterbox(image, new_shape=640)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to('cpu')
    img = img.float() / 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    return img

def postprocess_detections(detections, image):
    results = []
    for i, det in enumerate(detections):  # detections per image
        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], image.shape).round()
            for *xyxy, conf, cls in reversed(det):
                label = f'{model.names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, image, label=label, color=(0, 255, 0), line_thickness=2)
                result = {
                    "label": model.names[int(cls)],
                    "confidence": float(conf),
                    "box": [float(coord) for coord in xyxy]
                }
                results.append(result)
    return results

@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    image = Image.open(file.stream)
    image = np.array(image)

    img = preprocess_image(image)
    pred = model(img, augment=False)[0]
    pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)

    results = postprocess_detections(pred, image)

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
