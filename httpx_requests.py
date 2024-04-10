from httpx import AsyncClient, Response
from loguru import logger
 

@logger.catch
async def post_request(aclient: AsyncClient, url: str, parameters: any) -> Response:
    response = await aclient.post(url, json=parameters)
    return response


@logger.catch
async def get_request_alter(aclient: AsyncClient, base_url: str, parameters: dict[str: str | list[str]]) -> Response:
    if parameters:
        url = base_url + "?"
        for key, value in parameters.items():
            url += f"{key}={value}&"
        response = await aclient.get(url[:-1].replace(" ", "%20"))
    else:
        response = await aclient.get(base_url)
    return response


@logger.catch
async def get_request(aclient: AsyncClient, base_url: str, parameters: dict[str: str | list[str]]) -> Response:
    response = await aclient.get(base_url, params=parameters)
    return response


@logger.catch
async def put_request(aclient: AsyncClient, base_url: str, parameters: dict[str: str | list[str]]) -> Response:
    response = await aclient.put(base_url, params=parameters)
    return response


@logger.catch
async def patch_request(aclient: AsyncClient, base_url: str, parameters: dict[str: str | list[str]]) -> Response:
    response = await aclient.patch(base_url, params=parameters)
    return response


@logger.catch
async def delete_request(aclient: AsyncClient, url: str, params: dict[str: str]) -> Response:
    response = await aclient.delete(url, params=params)
    return response
