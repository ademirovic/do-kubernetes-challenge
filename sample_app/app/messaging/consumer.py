import io

import fastavro
from aiokafka import AIOKafkaConsumer


class Consumer:
    def __init__(self, url, topic, client_id, consumer_group, timeout):
        self.schema_dir = "app/messaging/schemas"
        self.schema = self._load_avro_schema()
        self.timeout = timeout
        self.messaging = AIOKafkaConsumer(
            topic,
            bootstrap_servers=url,
            client_id=client_id,
            group_id=consumer_group,
            value_deserializer=self._deserialize_avro,
        )

    async def start(self):
        await self.messaging.start()

    async def stop(self):
        await self.messaging.stop()

    async def getmany(self):
        data = await self.messaging.getmany(timeout_ms=self.timeout)
        return data

    def _deserialize_avro(self, item):
        return fastavro.schemaless_reader(io.BytesIO(item), self.schema)

    def _load_avro_schema(self):
        return fastavro.schema.load_schema_ordered(
            [f"{self.schema_dir}/Scoop.avsc", f"{self.schema_dir}/Purchase.avsc"]
        )
