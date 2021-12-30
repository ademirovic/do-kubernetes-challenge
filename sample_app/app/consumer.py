import asyncio
import io

from functools import partial

import aiokafka
import elasticsearch
import fastavro

from elasticsearch.helpers import async_bulk

from config import settings

es = elasticsearch.AsyncElasticsearch([settings.ELASTIC_URL])


def _deserialize_avro(item, schema):
    return fastavro.schemaless_reader(io.BytesIO(item), schema)


def _serialize_elastic(item):
    item["timestamp"] = item["timestamp"].isoformat()
    return item


async def send_to_elastic(data):
    for _tp, messages in data.items():
        for message in messages:
            yield {
                "_index": f"{settings.ELASTIC_INDEX}-{message.value['timestamp'].date().isoformat()}",
                "doc": {"data": _serialize_elastic(message.value)},
            }


async def consume():
    avro_schema = fastavro.schema.load_schema_ordered(
        ["app/schemas/Scoop.avsc", "app/schemas/Purchase.avsc"]
    )
    consumer = aiokafka.AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_URL,
        client_id=settings.KAFKA_CLIENT_ID,
        group_id=settings.KAFKA_CONSUMER_GROUP,
        value_deserializer=partial(_deserialize_avro, schema=avro_schema),
    )

    await consumer.start()

    try:
        while True:
            data = await consumer.getmany(timeout_ms=settings.KAFKA_CONSUMER_TIMEOUT_MS)
            if len(data) != 0:
                await async_bulk(es, send_to_elastic(data))
    finally:
        await consumer.stop()
        await es.close()


asyncio.run(consume())
