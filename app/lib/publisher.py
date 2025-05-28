import os
import pika
import json
import logging
from .queues import OUTPUT_QUEUES, CREATED_QUEUES

rabbitmq_ttl_dlx = int(os.getenv('RABBITMQ_TTL_DLX', 60000))  # 60 segundos

def ensure_queues_exist(channel):
    for queue in OUTPUT_QUEUES:
        channel.queue_declare(queue=queue, durable=True)
        logging.info(f"Queue '{queue}' checked or created.")

    for queue_pair in CREATED_QUEUES:
        main_queue, dlx_queue = queue_pair.split(',')

        channel.queue_declare(queue=main_queue, durable=True)
        logging.info(f"Queue '{main_queue}' checked or created.")

        declare_reprocess_queue(channel, dlx_queue, main_queue)
        logging.info(f"Queue '{main_queue}' and DLX queue '{dlx_queue}' checked or created.")

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

def declare_reprocess_queue(channel, reprocess_queue_name, dead_letter_queue_name):
    try:
        channel.queue_declare(
            queue=reprocess_queue_name,
            durable=True,
            arguments={
                'x-message-ttl': rabbitmq_ttl_dlx,
                'x-dead-letter-exchange': '',
                'x-dead-letter-routing-key': dead_letter_queue_name
            }
        )
        logging.info(f"Queue '{reprocess_queue_name}' declared with TTL and DLX.")
    except Exception as e:
        logging.error(f"Error declaring reprocess queue '{reprocess_queue_name}': {str(e)}")
