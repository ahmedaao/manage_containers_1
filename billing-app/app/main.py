import json
import os
import asyncio
import asyncpg
import aio_pika
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL config
BILLING_DB_HOST = os.getenv('BILLING_DB_HOST')
BILLING_DB_NAME = os.getenv('BILLING_DB_NAME')
BILLING_DB_USER = os.getenv('BILLING_DB_USER')
BILLING_DB_PASSWORD = os.getenv('BILLING_DB_PASSWORD')
BILLING_DB_PORT = int(os.getenv('BILLING_DB_PORT'))

# RabbitMQ config
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT'))
QUEUE_NAME = os.getenv('QUEUE_NAME')

# Async PostgreSQL connection
async def connect_db():
    return await asyncpg.connect(
        host=BILLING_DB_HOST,
        port=BILLING_DB_PORT,
        user=BILLING_DB_USER,
        password=BILLING_DB_PASSWORD,
        database=BILLING_DB_NAME
    )

# Callback for each message
async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():  # auto ack
        try:
            data = json.loads(message.body.decode())

            user_id = int(data["user_id"])
            number_of_items = int(data["number_of_items"])
            total_amount = float(data["total_amount"])

            conn = await connect_db()
            await conn.execute("""
                INSERT INTO orders (user_id, number_of_items, total_amount)
                VALUES ($1, $2, $3)
            """, user_id, number_of_items, total_amount)
            await conn.close()

            print(f"Processed order: user_id={user_id}, items={number_of_items}, amount={total_amount:.2f}")

        except Exception as e:
            print(f"Error processing message: {e}")

# Main async logic
async def start_consumer():
    connection = await aio_pika.connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
    )
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    print("Waiting for messages...")
    await queue.consume(process_message)

    await asyncio.Future()  # keep running

# Run the consumer directly
asyncio.run(start_consumer())