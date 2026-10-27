import asyncio
import logging

from amqtt.client import MQTTClient
from amqtt.mqtt.constants import QOS_0

"""
This sample shows how to publish messages to broker using QOS=0
"""

logger = logging.getLogger(__name__)


async def test_coro1() -> None:
    client = MQTTClient(config={"auto_reconnect": True})
    await client.connect("mqtt://localhost:1883/")
    tasks = [
        asyncio.ensure_future(client.publish("temperature", b"12", qos=0x00))
    ]
    await asyncio.wait(tasks)
    logger.info("Messages published")
    await client.disconnect()


def __main__():

    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)

    asyncio.run(test_coro1())

if __name__ == "__main__":
    __main__()
