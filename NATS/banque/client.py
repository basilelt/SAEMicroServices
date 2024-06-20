import asyncio
import nats

async def publisher():
    nc = await nats.connect("192.168.164.130:4222")

    counter = "client1.vol&Cie.147"
    await nc.publish("banque.client1.compte", str(counter).encode())
    print(f"Published: {counter}")
    await asyncio.sleep(10)

    await nc.close()

if __name__ == '__main__':
    asyncio.run(publisher())