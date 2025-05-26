import json
import time
import logging
from .publisher import send_to_queues, ensure_queues_exist
from .queues import INPUT_QUEUES
from .rabbitmq import connect_to_rabbitmq

def process_queue(connection, queue_name):
    channel = connection.channel()
    for method_frame, _, body in channel.consume(queue=queue_name, inactivity_timeout=1):
        if method_frame:
            message = json.loads(body.decode())
            logging.info(f"Message received from queue {queue_name}: {message['text']}, {message['level']}")
            send_to_queues(channel, message)
            channel.basic_ack(method_frame.delivery_tag)
        else:
            break
    channel.close()

def consume_messages():
    connection = connect_to_rabbitmq()
    if connection is None:
        logging.error("Connection to RabbitMQ failed. Exiting.")
        return

    setup_channel = connection.channel()
    ensure_queues_exist(setup_channel)
    setup_channel.close()

    for queue in INPUT_QUEUES:
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        logging.info(f"Queue '{queue}' checked or created.")
        channel.close()

    logging.info("Waiting for messages with priority for error queue...")

    try:
        while True:
            process_queue(connection, '00_syrin_notification_critical')
            process_queue(connection, '00_syrin_notification_warning')
            time.sleep(1)
    except Exception as e:
        logging.error(f"Error in message consumption: {str(e)}")
    finally:
        if connection and connection.is_open:
            connection.close()
            logging.info("Connection to RabbitMQ closed.")
