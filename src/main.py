from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import shutil
import os
import cv2

app = FastAPI()

# تحميل الموديل مرة واحدة
MODEL_PATH = os.getenv("MODEL_PATH", "weights/best.pt")
model = YOLO(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{file.filename}"

    # حفظ الصورة
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # تشغيل الموديل
    results = model(file_path)

    boxes = []
    for r in results:
        for box in r.boxes:
            boxes.append({
                "class": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    return {
        "detections": boxes,
        "count": len(boxes)
    }