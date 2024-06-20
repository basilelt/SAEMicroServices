import asyncio
import nats

async def cb(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print(f"Message reçu sur le sujet {subject} : {data}")
    response = f"Réponse pour le sujet {subject} avec les données {data}"
    await nc.publish(reply, response.encode())

async def mafonction():
    global nc
    nc = await nats.connect("192.168.164.130:4222")
    try:
        msg = await nc.subscribe("banque.*.compte",cb=cb)
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.close()

if __name__ == '__main__':
    asyncio.run(mafonction())