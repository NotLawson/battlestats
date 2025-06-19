FROM python:3.11-slim

WORKDIR /usr/app

COPY modules modules
COPY config.json .
COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]