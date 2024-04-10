from httpx import post, get, delete, AsyncClient
import asyncio


async def post_request(url, parameters):
    async with AsyncClient() as client:
        response = await client.post(url, json=parameters)
    return response


async def get_request(url, parameters):
    async with AsyncClient() as client:
        response = await client.get(url, json=parameters)
    return response


async def main():
    url = "http://localhost:8000/pdf/pdf_paths"
    parameters = {"pdf paths": [r"C:\Users\DXD\Desktop\exposing7feb2017.pdf",
                                r"C:\Users\DXD\Desktop\Order Confirmation.pdf"]}
    response = await post_request(url, parameters)
    print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
