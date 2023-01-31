import fastavro


class Messaging:
    def __init__(self):
        self.schema_dir = "app/messaging/schemas"
        self.schema = self._load_avro_schema()
        self.messaging = None

    async def start(self):
        await self.messaging.start()

    async def stop(self):
        await self.messaging.stop()

    def _load_avro_schema(self):
        return fastavro.schema.load_schema_ordered(
            [f"{self.schema_dir}/Scoop.avsc", f"{self.schema_dir}/Purchase.avsc"]
        )
