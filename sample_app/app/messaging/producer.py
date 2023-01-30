import io

import fastavro

from aiokafka import AIOKafkaProducer

from messaging.messaging import Messaging


class Producer(Messaging):
    def __init__(self, url, topic, client_id):
        super().__init__()
        self.topic = topic
        self.messaging = AIOKafkaProducer(
            client_id=client_id,
            bootstrap_servers=url,
            value_serializer=self._serialize_avro,
        )

    async def send_and_wait(self, item):
        await self.messaging.send_and_wait(self.topic, item)

    def _serialize_avro(self, item):
        buffer = io.BytesIO()
        fastavro.schemaless_writer(buffer, self.schema, item)
        buffer.seek(0)
        return buffer.read()
