FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./adaptor /app/adaptor
COPY ./utils /app/utils
COPY ./main.py /app/main.py

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:3000", "main:app" ]