# ── Stage: base ───────────────────────────────────────────────────────────────
# python:3.11-slim = صغير + مستقر، متستخدمش latest عشان بيتغير
FROM python:3.11-slim

# ── System deps ───────────────────────────────────────────────────────────────
# libgl1 + libglib2.0 = مطلوبين لـ OpenCV حتى لو headless
# بدونهم هتاخد: ImportError: libGL.so.1: cannot open shared object file
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Working dir ───────────────────────────────────────────────────────────────
WORKDIR /app

# ── Python deps ───────────────────────────────────────────────────────────────
# انسخ requirements الأول لوحده عشان Docker يعمل cache للـ layer دي
# لو بس غيرت كود، مش هيعيد install المكاتب من الأول
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── App code ──────────────────────────────────────────────────────────────────
COPY . .

# ── Weights folder (placeholder) ──────────────────────────────────────────────
RUN mkdir -p weights

# ── Expose ports ──────────────────────────────────────────────────────────────
EXPOSE 8000 8501

# ── Default: run FastAPI ───────────────────────────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
