import asyncio

from config import settings
from elastic_wrapper.elasticsearch_wrapper import ElasticSearchWrapper
from messaging.consumer import Consumer


async def consume():
    elastic_search = ElasticSearchWrapper(settings.ELASTIC_URL, settings.ELASTIC_INDEX)
    consumer = Consumer(
        settings.KAFKA_URL,
        settings.KAFKA_TOPIC,
        settings.KAFKA_CLIENT_ID,
        settings.KAFKA_CONSUMER_GROUP,
        settings.KAFKA_CONSUMER_TIMEOUT_MS,
    )
    await consumer.start()

    try:
        while True:
            data = await consumer.getmany()
            if len(data) != 0:
                await elastic_search.async_bulk(data)
    finally:
        await consumer.stop()
        await elastic_search.stop()


asyncio.run(consume())
