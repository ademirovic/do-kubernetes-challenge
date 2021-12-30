# Digital Ocean Kubernetes Challenge Sample App

An analytics demo data pipeline that collects ice cream purchase events.

Demo was built for [2021 digital ocean kubernetes challenge](https://www.digitalocean.com/community/pages/kubernetes-challenge) task:
```
Deploy a scalable message queue
A critical component of all the scalable architectures are message queues used to store and distribute
messages to multiple parties and introduce buffering. Kafka is widely used in this space and there are
multiple operators like Strimzi or to deploy it. For this project, use a sample app to demonstrate how
your message queue works.
```

A simple data processing pipeline provided an ideal use case for a sample app that uses a scalable message queue.

## Flow
- Ice creams puchase events are sent to API endpoint (`POST` purchases)
- Events are forwarded directly to Kafka
- Kafka consumers process and store the events to elasticsearch
- All stored events can be fetched from elasticsearch via `GET` purchases API call


## Local development
- Run docker-compose to start elasticsearch, kafka, kibana and zookeeper
```
docker-compose up -d
```
- Create an `.env` file (example: `.env.example`)
- Install project dependencies with [poetry](https://python-poetry.org/)
- Start API
```
uvicorn  app.main:app --reload
```
- Run consumer
```
python app/consumer.py
```
- Visit API docs and execute examples: http://localhost:8000/docs
- Or use curl:
```
# Send metrics example
curl -X 'POST' \
  'http://localhost:8000/purchases/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "shop_id": "9231c55f-b16c-45b8-b71e-731521495046",
  "purchase_id": "a430ef3a-86f3-4132-9474-a87c448fdb49",
  "timestamp": "2021-12-28 12:00:00+00",
  "scoops": [
    {
      "type": "chocolate",
      "quantity": 2,
      "price": 200
    }
  ]
}'
```


```
# Get metrics example
curl -X 'GET' \
  'http://localhost:8000/purchases/9231c55f-b16c-45b8-b71e-731521495046?date=2021-12-28' \
  -H 'accept: application/json'
```
