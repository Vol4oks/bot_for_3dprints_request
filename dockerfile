FROM python:3.9.9

WORKDIR /scr
COPY requirements.txt /scr
RUN pip install -r requirements.txt
COPY . /scr

