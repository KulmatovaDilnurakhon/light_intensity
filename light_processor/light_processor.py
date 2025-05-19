import pika

SOURCE_QUEUE = "lightIntensityQueue"
ALERT_QUEUE = "lightAlertQueue"

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue=SOURCE_QUEUE)
    channel.queue_declare(queue=ALERT_QUEUE)

    low_light_streak = 0

    def callback(ch, method, properties, body):
        nonlocal low_light_streak
        lux = int(body.decode())

        print(f"[Processor] Received lux: {lux}", flush=True)

        if lux < 100:
            low_light_streak += 1
            print(f"[Processor] Low light detected! Count = {low_light_streak}", flush=True)
        else:
            low_light_streak = 0

        if low_light_streak >= 3:
            alert = "Low light alert: 3 consecutive readings below 100 lux"
            channel.basic_publish(exchange='',
                                  routing_key=ALERT_QUEUE,
                                  body=alert)
            print(f"[Processor] ALERT SENT: {alert}", flush=True)
            low_light_streak = 0  # Reset after sending alert

    channel.basic_consume(queue=SOURCE_QUEUE,
                          on_message_callback=callback,
                          auto_ack=True)

    print('[Processor] Waiting for lux readings...', flush=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()