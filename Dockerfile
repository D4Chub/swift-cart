FROM python:3.11

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
    