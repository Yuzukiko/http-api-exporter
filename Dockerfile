FROM python:3.8.2-alpine

COPY ./app.py /
COPY ./requirements.txt /

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]