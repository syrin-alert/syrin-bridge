import pika
import json
import logging

from .queues import OUTPUT_QUEUES

def ensure_queues_exist(channel):
    for queue in OUTPUT_QUEUES:
        channel.queue_declare(queue=queue, durable=True)
        logging.info(f"Queue '{queue}' checked or created.")

def send_to_queues(channel, message):
    try:
        for queue in OUTPUT_QUEUES:
            channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=json.dumps(message, ensure_ascii=False),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            logging.info(f"Message sent to '{queue}': {message}")
    except Exception as e:
        logging.error(f"Error sending message to queues: {str(e)}")
