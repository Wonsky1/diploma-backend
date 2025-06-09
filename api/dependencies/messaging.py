from typing import Annotated
from fastapi import Depends
from clients.rabbitmq import get_rabbitmq_client, RabbitMQClient


RabbitMQClientDep = Annotated[RabbitMQClient, Depends(get_rabbitmq_client)]
