import json
import os
import pika
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BILLING_DB_HOST = os.getenv('BILLING_DB_HOST')
BILLING_DB_NAME = os.getenv('BILLING_DB_NAME')
BILLING_DB_USER = os.getenv('BILLING_DB_USER')
BILLING_DB_PASSWORD = os.getenv('BILLING_DB_PASSWORD')
BILLING_DB_PORT = int(os.getenv('BILLING_DB_PORT'))

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT'))
QUEUE_NAME = os.getenv('QUEUE_NAME')

def connect_db():
    """Connect to PostgreSQL"""
    return psycopg2.connect(
        host=BILLING_DB_HOST,
        database=BILLING_DB_NAME,
        user=BILLING_DB_USER,
        password=BILLING_DB_PASSWORD,
        port=BILLING_DB_PORT
    )

def connect_rabbitmq():
    """Connect to RabbitMQ without credentials"""
    # credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return connection, channel

def process_message(ch, method, properties, body):
    """Process a single message from billing_queue"""
    try:
        message = json.loads(body.decode('utf-8'))
        
        user_id = int(message['user_id'])
        number_of_items = int(message['number_of_items'])
        total_amount = float(message['total_amount'])

        db_conn = connect_db()
        cursor = db_conn.cursor()
        cursor.execute("""
            INSERT INTO orders (user_id, number_of_items, total_amount)
            VALUES (%s, %s, %s)
        """, (user_id, number_of_items, total_amount))
        db_conn.commit()

        cursor.close()
        db_conn.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[✓] Processed order: user_id={user_id}, items={number_of_items}, amount={total_amount:.2f}")

    except Exception as e:
        print(f"[!] Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

# Connect to RabbitMQ
connection, channel = connect_rabbitmq()

# Start consuming messages
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)

print("Waiting for messages...")
channel.start_consuming()