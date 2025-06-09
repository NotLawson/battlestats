FROM python:3

WORKDIR /usr/task_runner
COPY requirements.txt .
COPY modules .
COPY task_runner.py .
COPY config.json .

RUN pip3 install -r requirements.txt

CMD python3 task_runner.py


