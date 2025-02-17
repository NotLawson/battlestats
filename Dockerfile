FROM python:3

WORKDIR /usr/app

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]