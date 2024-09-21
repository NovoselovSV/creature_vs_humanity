FROM python:3.12.4

WORKDIR /app

RUN pip install gunicorn==23.0.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips", "*",  "--proxy-headers"]
