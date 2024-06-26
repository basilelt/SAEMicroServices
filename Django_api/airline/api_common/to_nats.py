# nats_utils.py

import asyncio
from nats.aio.client import Client as NATS

async def request_message(subject, message, servers, timeout=0.5):
    """
    Send a request message to a NATS server and wait for a response.

    Args:
        subject (str): The subject to publish the message to.
        message (str): The message to be sent.
        servers (str): The NATS server(s) to connect to.
        timeout (float): The time in seconds to wait for a response (default is 0.5).

    Returns:
        str: The response message received from the NATS server, or None if an exception occurs.
    """
    nc = NATS()
    await nc.connect(servers, user="user", password="password")

    try:
        response = await nc.request(subject, message.encode(), timeout=timeout)
        response = response.data.decode()
        return response
    except Exception:
        return None
    finally:
        await nc.drain()
        await nc.close()

async def post_message(subject, message, servers, timeout=5):
    """
    Post a message to a NATS server.

    Args:
        subject (str): The subject to publish the message to.
        message (str): The message to be sent.
        servers (str): The NATS server(s) to connect to.
        timeout (float): The time in seconds to wait for the publish to complete (default is 5).

    Returns:
        None: Returns None if an exception occurs.
    """
    nc = NATS()
    await nc.connect(servers, user="user", password="password")

    try:
        await nc.publish(subject, message.encode(), timeout=timeout)
    except Exception:
        return None
    finally:
        await nc.drain()
        await nc.close()
