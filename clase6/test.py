import asyncio, httpx

async def main():
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[client.get("http://127.0.0.1:8000/incrementar") for _ in range(100)])

asyncio.run(main())

