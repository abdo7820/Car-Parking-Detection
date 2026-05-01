# 🅿️ Smart Parking Detection System

> Real-time parking occupancy detection using **YOLOv8m** fine-tuned on a custom dataset.
> Deployed with **FastAPI + Streamlit + Docker**.

---

## 📊 Results

### Before vs After Fine-Tuning

| Metric | Before (Pretrained) | After (Fine-Tuned) | Improvement |
|--------|--------------------|--------------------|-------------|
| mAP50 | 0.0001 | **0.8825** | +0.8824 |
| mAP50-95 | 0.0000 | **0.7717** | +0.7717 |
| Precision | 0.0102 | **0.9589** | +0.9487 |
| Recall | 0.0013 | **0.8064** | +0.8051 |

> YOLOv8m pretrained had near-zero performance on parking data —
> confirming the model had never seen this domain.
> Fine-tuning brought mAP50 from ~0 → **0.8825**.

---

### Model Comparison

| Model | mAP50 | Precision | Recall | FPS | Size |
|-------|-------|-----------|--------|-----|------|
| YOLOv8m pretrained | 0.0001 | 0.0102 | 0.0013 | 44.8 | 52.0 MB |
| YOLOv8n fine-tuned | 0.8644 | 0.9345 | 0.8139 | **134.7** | **6.2 MB** |
| YOLOv8m fine-tuned ⭐ | **0.8825** | **0.9589** | 0.8064 | 44.8 | 52.0 MB |

**Chosen model: YOLOv8m fine-tuned**
- +0.018 mAP50 over YOLOv8n
- +0.024 Precision over YOLOv8n
- 44.8 FPS — suitable for server deployment

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/parking-detection
cd parking-detection

# 2. Add trained weights
cp best.pt weights/best.pt

# 3. Run
docker compose up --build
```

- **Frontend** → http://localhost:8501
- **API Docs** → http://localhost:8000/docs

---

## 🗂️ Project Structure

```
parking-detection/
│
├── app/
│   ├── main.py              # FastAPI backend
│   └── model.py             # YOLOv8 inference logic
│
├── weights/
│   └── best.pt              # Trained weights (see Download)
│
├── results/
│   ├── confusion_matrix.png
│   ├── PR_curve.png
│   ├── F1_curve.png
│   └── model_comparison.csv
│
├── train.ipynb              # Full training notebook (Kaggle)
├── streamlit_app.py         # Frontend UI
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🧠 Approach

### 1. Dataset
- Annotated via **Roboflow**
- Augmentation: horizontal flip · rotation ±15° · brightness ±25%
- Classes: `empty`, `occupied`

### 2. Training
- Base model: `YOLOv8m.pt` pretrained on COCO
- Optimizer: **AdamW** + cosine LR scheduling
- Early stopping: patience = 20 epochs
- Tracked with **MLflow** — 5 runs logged

### 3. Experiment Tracking (MLflow)

| Run | Description | Key Metric |
|-----|-------------|------------|
| `01_baseline_yolov8m_pretrained` | Before fine-tuning | mAP50: 0.0001 |
| `02_finetuned_yolov8m` | After fine-tuning + artifacts | mAP50: 0.8825 |
| `03_finetuned_yolov8n` | Comparison model | mAP50: 0.8644 |
| `04_model_comparison_summary` | Final comparison table | — |
| `05_onnx_export` | ONNX benchmark | 43.3 FPS |

### 4. Export
- Exported to **ONNX** (opset 17, simplified) — 103.6 MB
- Runs with ONNX Runtime 1.25.1 (CUDAExecutionProvider)
- PyTorch: 44.6 FPS · ONNX: 43.3 FPS on same GPU

---
## 🐳 Docker Architecture

```
User Browser
     │
     ▼
[Streamlit :8501]  ──HTTP──▶  [FastAPI :8000]
    Frontend                     Backend
  (UI + upload)              (YOLO inference)
                                   │
                              weights/best.pt
```

---

## 📦 Download Weights

Too large for GitHub — download from Google Drive:

> **[best.pt — 52 MB](https://drive.google.com/YOUR_LINK)**
> **[best.onnx — 103.6 MB](https://drive.google.com/YOUR_LINK)**

Place in `weights/` before running.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| YOLOv8m | Object detection model |
| Roboflow | Dataset & augmentation |
| MLflow | Experiment tracking |
| FastAPI | REST API backend |
| Streamlit | Frontend UI |
| Docker | Containerization |
| ONNX Runtime 1.25.1 | Cross-platform export |
| Kaggle P100 | Training GPU |

---

## 📋 API

### `GET /health`
```json
{ "status": "ok", "model_loaded": true }
```

### `POST /detect`
**Request:** `multipart/form-data` — `file` (JPEG/PNG)

**Response:**
```json
{
  "total_detections": 12,
  "occupied_spots": 8,
  "free_spots": 4,
  "detections": [
    { "bbox": [100,150,200,280], "confidence": 0.95, "class_name": "occupied" }
  ],
  "annotated_image": "<base64>"
}
```

---

## 🔧 Run Locally

```bash
pip install -r requirements.txt

# Terminal 1
uvicorn app.main:app --reload

# Terminal 2
streamlit run streamlit_app.py
```

---

## 👤 Author

**Your Name**
🔗 **LinkedIn:** https://www.linkedin.com/in/abdulrah-manmohamed-yousry
💻 **GitHub:** https://github.com/abdo7820

