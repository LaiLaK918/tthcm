FROM python:3.12-slim

RUN apt-get update && \
  apt-get install -y \
  build-essential \
  meson \
  ninja-build \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "chainlit run main.py  --port 80 --host 0.0.0.0"]
