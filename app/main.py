import os
import pika
import json
import logging
import time

# Configure INFO level logging
logging.basicConfig(level=logging.INFO)

# Disable pika debug logs, setting them to WARNING or higher
logging.getLogger("pika").setLevel(logging.WARNING)

# Load RabbitMQ settings from environment variables
rabbitmq_host = os.getenv('RABBITMQ_HOST', '')
rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
rabbitmq_vhost = os.getenv('RABBITMQ_VHOST', '')
rabbitmq_user = os.getenv('RABBITMQ_USER', '')
rabbitmq_pass = os.getenv('RABBITMQ_PASS', '')

def connect_to_rabbitmq():
    try:
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
        client_properties = {"connection_name": "Syrin Message Distributor Agent"}
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host=rabbitmq_vhost,
            credentials=credentials,
            client_properties=client_properties
        )
        return pika.BlockingConnection(parameters)
    except Exception as e:
        logging.error(f"Error connecting to RabbitMQ: {str(e)}")
        return None

def ensure_queues_exist(channel):
    """Ensure that required queues are declared before processing messages."""
    queues_to_declare = ['01_syrin_notification_audio_process', '01_syrin_notification_message_process', '02_syrin_notification_message_process_humanized']
    for queue in queues_to_declare:
        channel.queue_declare(queue=queue, durable=True)
        logging.info(f"Queue '{queue}' checked or created.")

def send_to_queues(channel, message):
    try:
        # Publish message to both queues        
        channel.basic_publish(
            exchange='',
            routing_key='02_syrin_notification_message_process_humanized',
            body=json.dumps(message, ensure_ascii=False),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        logging.info(f"Message sent to '02_syrin_notification_message_process_humanized' queue: {message}")
                
        channel.basic_publish(
            exchange='',
            routing_key='01_syrin_notification_audio_process',
            body=json.dumps(message, ensure_ascii=False),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        logging.info(f"Message sent to '01_syrin_notification_audio_process' queue: {message}")

        channel.basic_publish(
            exchange='',
            routing_key='01_syrin_notification_message_process',
            body=json.dumps(message, ensure_ascii=False),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        logging.info(f"Message sent to '01_syrin_notification_message_process' queue: {message}")

    except Exception as e:
        logging.error(f"Error sending message to queues: {str(e)}")

def process_queue(connection, queue_name):
    """Process messages from a single queue until it is empty."""
    channel = connection.channel()
    for method_frame, _, body in channel.consume(queue=queue_name, inactivity_timeout=1):
        if method_frame:
            message = json.loads(body.decode())
            logging.info(f"Message received from queue {queue_name}: {message['text']}, {message['level']}")
            send_to_queues(channel, message)
            channel.basic_ack(method_frame.delivery_tag)
        else:
            # Exit the loop when there are no more messages in the queue
            break
    # Close the channel after processing
    channel.close()

def consume_messages():
    try:
        connection = connect_to_rabbitmq()
        if connection is None:
            logging.error("Connection to RabbitMQ failed. Exiting the application.")
            return

        # Create a channel to ensure the target queues exist
        setup_channel = connection.channel()
        ensure_queues_exist(setup_channel)
        setup_channel.close()

        # Declare all queues to ensure they exist before consuming
        for queue in ['00_syrin_notification_error', '00_syrin_notification_warning']:
            channel = connection.channel()
            channel.queue_declare(queue=queue, durable=True)
            logging.info(f"Queue '{queue}' checked or created.")
            channel.close()

        logging.info("Waiting for messages with priority for error queue...")

        while True:
            # Prioritize the error queue
            process_queue(connection, '00_syrin_notification_error')
            # Process warning queue only if the error queue is empty
            process_queue(connection, '00_syrin_notification_warning')
            time.sleep(1)  # Add a small delay to prevent continuous polling

    except Exception as e:
        logging.error(f"Error in message consumption: {str(e)}")
    finally:
        if connection and connection.is_open:
            connection.close()
            logging.info("Connection to RabbitMQ closed.")

if __name__ == "__main__":
    try:
        logging.info("Message Distributor with Priority - started \o/")
        consume_messages()
    except Exception as e:
        logging.error(f"Error running the application: {str(e)}")