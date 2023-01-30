import fastavro
import io

from aiokafka import AIOKafkaProducer


class Producer:
    def __init__(self, url, topic, client_id) -> None:
        self.schema_dir = "app/messaging/schemas"
        self.schema = self._load_avro_schema()
        self.topic = topic
        self.messaging = AIOKafkaProducer(
            client_id=client_id,
            bootstrap_servers=url,
            value_serializer=self._serialize_avro,
        )

    async def start(self):
        await self.messaging.start()

    async def stop(self):
        await self.messaging.stop()

    async def send_and_wait(self, item):
        await self.messaging.send_and_wait(self.topic, item)

    def _serialize_avro(self, item):
        buffer = io.BytesIO()
        fastavro.schemaless_writer(buffer, self.schema, item)
        buffer.seek(0)
        return buffer.read()

    def _load_avro_schema(self):
        return fastavro.schema.load_schema_ordered(
            [f"{self.schema_dir}/Scoop.avsc", f"{self.schema_dir}/Purchase.avsc"]
        )
