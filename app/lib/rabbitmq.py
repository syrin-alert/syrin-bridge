import os
import pika
import logging

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
