FROM python:3.11
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .