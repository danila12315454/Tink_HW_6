import json
from typing import Awaitable, Callable, Dict

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from . import schemas
from .data_manager import DataManager

app = FastAPI()

data_manager = DataManager()


async def set_body(request: Request, body: bytes) -> None:
    async def receive() -> Dict[str, str | bytes]:
        return {"type": "http.request", "body": body}

    request._receive = receive  # pylint: disable=W0212


async def get_body(request: Request) -> Dict[str, str]:
    body = await request.body()
    await set_body(request, body)
    dict_body: Dict[str, str] = json.loads(body)
    return dict_body


@app.middleware("http")
async def content_type_checker(
    request: Request, call_next: Callable[[Request], Awaitable[JSONResponse]]
) -> JSONResponse:
    match str(request.url).rsplit('/', maxsplit=1)[-1]:
        case "set":
            await set_body(request, await request.body())
            request_body = await get_body(request)
            if request.headers["content-type"] != "application/json":
                return JSONResponse(
                    status_code=415,
                    content={"detail": "Unsupported Media Type"},
                )
            if ("key" not in request_body.keys()) or (
                "value" not in request_body.keys()
            ):
                return JSONResponse(
                    status_code=400, content={"detail": "Bad Request"}
                )
        case "divide":
            if request.headers["content-type"] != "application/json":
                return JSONResponse(
                    status_code=415,
                    content={"detail": "Unsupported Media Type"},
                )
    response = await call_next(request)
    return response


@app.get("/hello")
def hello_rout() -> Response:
    return Response("HSE One Love!", media_type="text/plain")


@app.post("/set")
def set_value(key_value: schemas.KeyValueSchema) -> Response:
    data_manager.set(key=key_value.key, value=key_value.value)
    return Response()


@app.get("/get/{key}")
def get_value(key: str) -> Response:
    if not data_manager.get(key):
        return JSONResponse(status_code=404, content=None)
    return JSONResponse(
        status_code=200,
        content={"key": key, "value": data_manager.get(key)},
    )


@app.post("/divide")
def divide(
    divider_dividend: schemas.DeviderDevidentSchema,
) -> Response:
    try:
        return Response(
            str(divider_dividend.dividend / divider_dividend.divider),
            media_type="text/plain",
        )
    except ZeroDivisionError:
        return JSONResponse(status_code=400, content=None)


@app.get("/{full_path:path}")
def not_allowed_routes() -> JSONResponse:
    return JSONResponse(status_code=405, content=None)
