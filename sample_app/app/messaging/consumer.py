import io

import fastavro
from aiokafka import AIOKafkaConsumer

from messaging.messaging import Messaging


class Consumer(Messaging):
    def __init__(self, url, topic, client_id, consumer_group, timeout):
        super().__init__()
        self.timeout = timeout
        self.messaging = AIOKafkaConsumer(
            topic,
            bootstrap_servers=url,
            client_id=client_id,
            group_id=consumer_group,
            value_deserializer=self._deserialize_avro,
        )

    async def getmany(self):
        data = await self.messaging.getmany(timeout_ms=self.timeout)
        return data

    def _deserialize_avro(self, item):
        return fastavro.schemaless_reader(io.BytesIO(item), self.schema)
