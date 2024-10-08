FROM python:3

WORKDIR /usr/battlestats

RUN pip3 install -r requirements.txt

CMD python3 main.py