import json
from logging import getLogger

from core.config import settings, Exchanges, Queues

import uuid
from aio_pika import Message, connect
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractQueue,
)
from aio_pika import exceptions


logger = getLogger(__name__)


class RabbitMQClient:
    EXCHANGES = settings.RABBITMQ_EXCHANGES
    QUEUES = settings.RABBITMQ_QUEUES
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue

    def __init__(self) -> None:
        self.connection = None
        self.channel = None
        self.callback_queue = None

    async def initialize(self) -> None:
        await self.connect()

    async def ensure_channel(self) -> None:
        """
        Ensures the channel is open and reconnects if it is closed.
        """
        if self.channel.is_closed:
            logger.warning("Channel is closed. Reconnecting...")
            await self.connect()

    async def connect(self) -> None:
        self.connection = await connect(url=settings.RABBITMQ_URL, retries=5)
        self.channel = await self.connection.channel()

        for exchange_name in self.EXCHANGES:
            await self.channel.declare_exchange(
                name=exchange_name,
                type="direct",
            )

            for queue in self.QUEUES:
                queue_name = f"{exchange_name}_{queue}"
                declared_queue = await self.channel.declare_queue(
                    name=queue_name, durable=True
                )
                await declared_queue.bind(
                    exchange=exchange_name,
                    routing_key=queue,
                )

    async def send_message(
        self, exchange: Exchanges, body: dict, message_id: str | None = None
    ) -> str:
        await self.ensure_channel()
        if message_id is None:
            message_id = str(uuid.uuid4())
        callback_queue = await self.channel.declare_queue(message_id, auto_delete=True)
        target_exchange = await self.channel.get_exchange(exchange)

        body["reply_to"] = callback_queue.name
        body = json.dumps(body).encode()

        await target_exchange.publish(
            Message(
                body=body,
                content_type="text/plain",
            ),
            routing_key=Queues.PENDING,
        )

        return message_id

    async def send_messages(
        self, exchange: Exchanges, bodies: list[dict], message_id: str | None = None
    ) -> str:
        await self.ensure_channel()
        if message_id is None:
            message_id = str(uuid.uuid4())

        callback_queue = await self.channel.declare_queue(message_id, auto_delete=True)
        target_exchange = await self.channel.get_exchange(exchange)

        for body in bodies:
            body["reply_to"] = callback_queue.name
            encoded_body = json.dumps(body).encode()

            await target_exchange.publish(
                Message(
                    body=encoded_body,
                    content_type="text/plain",
                ),
                routing_key=Queues.PENDING,
            )

        return message_id

    async def check_queue_messages_were_processed(
        self, message_id: str, expected_messages: int
    ) -> bool | None:
        await self.ensure_channel()
        try:
            queue: AbstractQueue = await self.channel.declare_queue(
                message_id, passive=True
            )

            queue_info = await queue.declare()
            message_count = queue_info.message_count

            return message_count == expected_messages

        except exceptions.QueueEmpty:
            return False

        except Exception as e:
            logger.error(f"Messages were already retrieved or wrong message id: {e}")
            return None

    async def get_messages(self, job_id: str) -> list[dict]:
        await self.ensure_channel()
        messages = []
        try:
            queue: AbstractQueue = await self.channel.declare_queue(
                job_id, passive=True
            )

            while True:
                message = await queue.get(timeout=1)
                if message is None:
                    break

                async with message.process():
                    body = json.loads(message.body.decode())
                    if message.headers:
                        body["headers"] = dict(message.headers)
                    messages.append(body)

            await queue.delete()
            return messages
        except exceptions.QueueEmpty:
            logger.info(f"Queue {job_id} is empty")
            await queue.delete()
            return messages
        except Exception as e:
            logger.error(f"Error getting messages from queue {job_id}: {e}")
            return messages

    async def close_connection(self) -> None:
        await self.connection.close()


_rabbitmq_client: RabbitMQClient | None = None


async def get_rabbitmq_client() -> RabbitMQClient:
    global _rabbitmq_client
    if not _rabbitmq_client:
        _rabbitmq_client = RabbitMQClient()
        await _rabbitmq_client.initialize()
    return _rabbitmq_client
