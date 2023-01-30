import datetime
import io

from functools import partial
from typing import Optional
from uuid import UUID

import fastavro

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import AsyncElasticsearch

from config import settings
from model import Purchase

app = FastAPI(title="Ice Cream Purchase Analytics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _serialize_avro(item, schema):
    buffer = io.BytesIO()
    fastavro.schemaless_writer(buffer, schema, item)
    buffer.seek(0)
    return buffer.read()


avro_schema = fastavro.schema.load_schema_ordered(
    ["app/schemas/Scoop.avsc", "app/schemas/Purchase.avsc"]
)

aioproducer = None
es = AsyncElasticsearch([settings.ELASTIC_URL])


@app.on_event("startup")
async def startup_event():
    global aioproducer
    aioproducer = AIOKafkaProducer(
        client_id=settings.KAFKA_CLIENT_ID,
        bootstrap_servers=settings.KAFKA_URL,
        value_serializer=partial(_serialize_avro, schema=avro_schema),
    )
    await aioproducer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()
    await es.close()


@app.get("/")
async def root():
    """Welcome message."""
    return {"message": "Welcome to Ice Cream Purchase Analytics"}


@app.post("/purchases/")
async def create_purchase(purchase: Purchase):
    """Create an ice cream purchase event."""
    await aioproducer.send_and_wait(settings.KAFKA_TOPIC, purchase.dict())
    return purchase


@app.get("/purchases/{shop_id}")
async def get_purchases(
    shop_id: UUID, date: Optional[datetime.date] = datetime.date.today()
):
    """Get ice cream purchase events of specific shop that happened on designated date."""
    index = f"{settings.ELASTIC_INDEX}-{date.isoformat()}"

    if not await es.indices.exists(index=index):
        return []

    result = await es.search(
        index=index,
        sort=[{"doc.data.timestamp": {"unmapped_type": "boolean", "order": "desc"}}],
        query={"match": {"doc.data.shop_id": shop_id}},
    )
    return result["hits"]["hits"]


@app.get("/healthz")
async def healthz():
    return "ok"
