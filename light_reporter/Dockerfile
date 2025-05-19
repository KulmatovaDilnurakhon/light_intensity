FROM python:3.10-slim

WORKDIR /app

COPY light_reporter.py .

RUN pip install pika

CMD ["python", "-u", "light_reporter.py"]