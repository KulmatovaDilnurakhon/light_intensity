import pika

ALERT_QUEUE = "lightAlertQueue"

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue=ALERT_QUEUE)

    def callback(ch, method, properties, body):
        alert_msg = body.decode()
        print(f"[Reporter] 🚨 ALERT: {alert_msg}", flush=True)

    channel.basic_consume(queue=ALERT_QUEUE,
                          on_message_callback=callback,
                          auto_ack=True)

    print('[Reporter] Waiting for alerts...', flush=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()