FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

# system deps for pdfplumber/pillow/tesseract (Debian)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential wget git libgl1 \
    libsm6 libxrender1 libxext6 poppler-utils tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
