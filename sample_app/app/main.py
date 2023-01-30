import datetime
import io

from functools import partial
from typing import Optional
from uuid import UUID


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from elastic_wrapper.elasticsearch_wrapper import ElasticSearchWrapper
from model import Purchase
from messaging.producer import Producer

app = FastAPI(title="Ice Cream Purchase Analytics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

producer = Producer(settings.KAFKA_URL, settings.KAFKA_TOPIC, settings.KAFKA_CLIENT_ID)
elastic_search = ElasticSearchWrapper(settings.ELASTIC_URL, settings.ELASTIC_INDEX)


@app.on_event("startup")
async def startup_event():
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()
    await elastic_search.stop()


@app.get("/")
async def root():
    """Welcome message."""
    return {"message": "Welcome to Ice Cream Purchase Analytics"}


@app.post("/purchases/")
async def create_purchase(purchase: Purchase):
    """Create an ice cream purchase event."""
    await producer.send_and_wait(purchase.dict())
    return purchase


@app.get("/purchases/{shop_id}")
async def get_purchases(
    shop_id: UUID, date: Optional[datetime.date] = datetime.date.today()
):
    """Get ice cream purchase events of specific shop that happened on designated date."""
    return await elastic_search.get_purchases(shop_id, date)


@app.get("/healthz")
async def healthz():
    return "ok"
