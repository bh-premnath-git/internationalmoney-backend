"""
Kafka helpers using aiokafka.

  await init_events()
  ...
  await publish("topic", {...})
  ...
  await close_events()
"""
import asyncio
import json
import os
from typing import Optional

from aiokafka import AIOKafkaProducer

_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
_producer: Optional[AIOKafkaProducer] = None


async def init_events():
    """Initialises the Kafka producer.

    Should be called once on application startup.
    """
    global _producer
    if _producer is not None:
        # Already initialised
        return

    _producer = AIOKafkaProducer(
        bootstrap_servers=_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode(),
    )
    await _producer.start()


async def close_events():
    """Closes the Kafka producer.

    Should be called once on application shutdown.
    """
    global _producer
    if _producer:
        await _producer.stop()
        _producer = None


async def publish(topic: str, payload: dict):
    if _producer is None:
        raise RuntimeError("Kafka producer not initialised – call init_events() first")
    await _producer.send_and_wait(topic, payload)
