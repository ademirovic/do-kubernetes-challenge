import asyncio
import io

from functools import partial

import aiokafka
import fastavro

from config import settings
from elastic_wrapper.elasticsearch_wrapper import ElasticSearchWrapper


def _deserialize_avro(item, schema):
    return fastavro.schemaless_reader(io.BytesIO(item), schema)


async def consume():
    elastic_search = ElasticSearchWrapper(settings.ELASTIC_URL, settings.ELASTIC_INDEX)
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
                await elastic_search.async_bulk(data)
    finally:
        await consumer.stop()
        await elastic_search.stop()


asyncio.run(consume())
