import pika
import random
import time

QUEUE_NAME = "lightIntensityQueue"

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    while True:
        lux = random.randint(0, 200)
        message = str(lux)
        channel.basic_publish(exchange='',
                              routing_key=QUEUE_NAME,
                              body=message)
        print(f"[Generator] Sent lux: {lux}", flush=True)
        time.sleep(3)

if __name__ == "__main__":
    main()
