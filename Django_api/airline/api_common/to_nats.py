# nats_utils.py
import asyncio
from nats.aio.client import Client as NATS
import time

async def request_message(subject, message, servers, timeout=0.5):
    nc = NATS()
    await nc.connect(servers,user="user",password="password")

    try:
        response = await nc.request(subject, message.encode())
        response = response.data.decode()
        #await nc.publish("banque.validation", response.encode())    
        return response
    except Exception :
        return None
    finally:
        await nc.drain()
        await nc.close()

async def post_message(subject, message, servers, timeout=5):
    nc = NATS()
    await nc.connect(servers,user="user",password="password")

    try:
        await nc.publish(subject, message.encode(), timeout=timeout)
    except Exception :
        return None
    finally:
        await nc.drain()
        await nc.close()