from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk


class ElasticSearchWrapper:
    def __init__(self, url, index):
        self.elastic_search = AsyncElasticsearch([url])
        self.index = index

    async def stop(self):
        await self.elastic_search.close()

    async def async_bulk(self, data):
        await async_bulk(self.elastic_search, self._yield_messages(data))

    async def get_purchases(self, shop_id, date):
        index = self._get_index(date)

        if not await self.elastic_search.indices.exists(index=index):
            return []

        result = await self.elastic_search.search(
            index=index,
            sort=[
                {"doc.data.timestamp": {"unmapped_type": "boolean", "order": "desc"}}
            ],
            query={"match": {"doc.data.shop_id": shop_id}},
        )
        return result["hits"]["hits"]

    async def _yield_messages(self, data):
        for _tp, messages in data.items():
            for message in messages:
                yield {
                    "_index": f"{self.index}-{message.value['timestamp'].date().isoformat()}",
                    "doc": {"data": self._serialize_elastic(message.value)},
                }

    def _get_index(self, date):
        return f"{self.index}-{date.isoformat()}"

    def _serialize_elastic(self, item):
        item["timestamp"] = item["timestamp"].isoformat()
        return item
