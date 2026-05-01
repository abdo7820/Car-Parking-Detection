# 🅿️ Smart Parking Detection System

Real-time parking occupancy detection using **YOLOv8** fine-tuned on a custom dataset.  
Stack: **FastAPI · Streamlit · Docker**

---

## Results

| Metric    | Score  |
|-----------|--------|
| mAP50     | —      |
| Precision | —      |
| Recall    | —      |
| FPS       | ~28    |

> Fill in your actual numbers after training.

---

## Project Structure

```
parking-detection/
├── app/
│   ├── main.py          # FastAPI backend
│   └── model.py         # YOLO inference
├── weights/             # Put best.pt here
├── streamlit_app.py     # Streamlit frontend
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Run with Docker (recommended)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/parking-detection
cd parking-detection

# 2. Add your trained weights
cp /path/to/best.pt weights/best.pt

# 3. Build and run
docker compose up --build

# Frontend → http://localhost:8501
# API docs → http://localhost:8000/docs
```

---

## Run locally (without Docker)

```bash
pip install -r requirements.txt

# Terminal 1 — Backend
uvicorn app.main:app --reload

# Terminal 2 — Frontend
streamlit run streamlit_app.py
```

---

## API Endpoints

| Method | Endpoint        | Description              |
|--------|-----------------|--------------------------|
| GET    | `/health`       | API status               |
| POST   | `/detect`       | Detect parking from image|

---

## Tech Stack

`Python` · `YOLOv8` · `FastAPI` · `Streamlit` · `OpenCV` · `Docker` · `Roboflow`
