FROM python:3.10

WORKDIR /bot

ADD main.py ./
ADD states.py ./
ADD models ./models
ADD requirements.txt ./

RUN pip3 install -r requirements.txt

CMD python3 main.py
