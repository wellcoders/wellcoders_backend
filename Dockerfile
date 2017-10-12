FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN yes s|pip install -r requirements.txt
