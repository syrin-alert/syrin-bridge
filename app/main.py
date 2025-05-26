import logging
from lib.consumer import consume_messages

logging.basicConfig(level=logging.INFO)
logging.getLogger("pika").setLevel(logging.WARNING)

if __name__ == "__main__":
    try:
        logging.info("Message Distributor with Priority - started \o/")
        consume_messages()
    except Exception as e:
        logging.error(f"Error running the application: {str(e)}")
