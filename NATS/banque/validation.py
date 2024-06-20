async def main():
    global nc
    nc = await nats.connect("nats://192.168.164.130:4222")
    try:
        await nc.subscribe("validation.place.client.*", cb=handle_place_validation)
        
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.close()


if __name__ == '__main__':
    asyncio.run(main())