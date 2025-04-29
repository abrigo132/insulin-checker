from taskiq_aio_pika import AioPikaBroker

# from .config import settings

broker = AioPikaBroker(url="amqp://guest:guest@localhost:5672//")
