FROM python:3.11-slim

WORKDIR /usr/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY modules modules
COPY static static
COPY templates templates
COPY config.json .
COPY main.py .


CMD ["python3", "main.py"]