from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import aiohttp
import json
import os
import aio_pika
from dotenv import load_dotenv

load_dotenv()

INVENTORY_API_URL = os.getenv("INVENTORY_API_URL")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
QUEUE_NAME = os.getenv("QUEUE_NAME")

app = FastAPI()

@app.api_route("/api/movies", methods=["GET", "POST", "DELETE"])
@app.api_route("/api/movies/{movie_id}", methods=["GET", "PUT", "DELETE"])
async def proxy_to_inventory(request: Request, movie_id: str = None):
    try:
        method = request.method
        headers = dict(request.headers)
        body = await request.body()

        url = INVENTORY_API_URL
        if movie_id:
            url += f"/{movie_id}"

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, data=body) as resp:
                content = await resp.read()
                return Response(
                    content=content,
                    status_code=resp.status,
                    media_type=resp.headers.get("content-type", "application/json")
                )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Send POST body to RabbitMQ (async with aio_pika)
@app.post("/api/billing")
async def billing_handler(request: Request):
    try:
        body = await request.json()
        message = json.dumps(body)

        connection = await aio_pika.connect_robust(f"amqp://{RABBITMQ_HOST}/")
        async with connection:
            channel = await connection.channel()

            # Declare the queue
            await channel.declare_queue(QUEUE_NAME, durable=True)

            # Publish the message
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=message.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=QUEUE_NAME
            )

        return {"message": "Message posted"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})