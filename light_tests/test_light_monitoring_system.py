import pika
import time
import unittest

LIGHT_QUEUE = 'lightIntensityQueue'
ALERT_QUEUE = 'lightAlertQueue'


class TestLightMonitoringSystem(unittest.TestCase):

    def setUp(self):
        # Connect to RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=LIGHT_QUEUE)
        self.channel.queue_declare(queue=ALERT_QUEUE)

        # Clear queues before each test
        self.channel.queue_purge(queue=LIGHT_QUEUE)
        self.channel.queue_purge(queue=ALERT_QUEUE)

    def tearDown(self):
        self.connection.close()

    def test_1_message_sending_and_receiving(self):
        """Test that light values are sent and received correctly."""

        test_value = "550"
        self.channel.basic_publish(
            exchange='',
            routing_key=LIGHT_QUEUE,
            body=test_value
        )

        # Consume the message
        method_frame, header_frame, body = self.channel.basic_get(LIGHT_QUEUE, auto_ack=True)
        self.assertIsNotNone(body)
        self.assertEqual(body.decode(), test_value)

    def test_2_low_light_detection(self):
        """Send 3 consecutive low-light values and verify an alert is generated."""

        low_values = ["50", "80", "60"]
        for val in low_values:
            self.channel.basic_publish(exchange='', routing_key=LIGHT_QUEUE, body=val)
            time.sleep(1)  # Let processor consume and evaluate

        # Allow time for processor to react
        time.sleep(5)

        method_frame, header_frame, body = self.channel.basic_get(ALERT_QUEUE, auto_ack=True)
        self.assertIsNotNone(body)
        self.assertIn("Low light alert", body.decode())

    def test_3_alert_reporting(self):
        """Send alert to alert queue and confirm it can be received (simulates reporter)."""

        alert_message = "Low light alert: 3 consecutive readings below 100 lux"
        self.channel.basic_publish(
            exchange='',
            routing_key=ALERT_QUEUE,
            body=alert_message
        )

        method_frame, header_frame, body = self.channel.basic_get(ALERT_QUEUE, auto_ack=True)
        self.assertIsNotNone(body)
        self.assertEqual(body.decode(), alert_message)


if __name__ == '__main__':
    unittest.main()