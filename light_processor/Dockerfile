FROM python:3.10-slim

WORKDIR /app

COPY light_processor.py .

RUN pip install pika

CMD ["python", "-u", "light_processor.py"]