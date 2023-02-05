__all__ = ("accept", "ip", "user_agent")

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, PlainTextResponse
from orjson import dumps


def _prepare_response(request: Request, key: str, value: str) -> Response:
    media_types = [
        media_type.split(";q=") if ";" in media_type else [media_type, 1.0]
        for media_type in request.headers.get("accept").split(",")
    ]
    media_types.sort(key=lambda media_type: float(media_type[1]), reverse=True)

    for media_type, priority in media_types:
        print(media_type)
        match media_type:
            case "*/*" | "text/plain":
                return PlainTextResponse(value)
            case "application/javascript":
                callback = (
                    request.query_params.get("callback")
                    if request.query_params.get("callback")
                    else "callback"
                )

                return Response(
                    f"{callback}({dumps({key: value})});".encode("utf-8"),
                    media_type="application/javascript",
                )
            case "application/json":
                return Response(dumps({key: value}), media_type="application/json")
            # case "application/xml":
            #     return Response()
    else:
        raise HTTPException(status_code=406)


def accept(request: Request) -> Response:
    return _prepare_response(request, "accept", request.headers.get("accept"))


def ip(request: Request) -> Response:
    # Add correct parsing
    request_ip = request.headers.get("x-forwarded-for", request.client.host)

    return _prepare_response(request, "ip", request_ip)


def user_agent(request: Request) -> Response:
    return _prepare_response(request, "user-agent", request.headers.get("user-agent"))
