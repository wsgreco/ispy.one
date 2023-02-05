from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
import api


def homepage(request: Request) -> HTMLResponse:
    return HTMLResponse("More coming soon!")


routes = (
    Route("/", homepage),
    Mount(
        "/v1",
        routes=[
            Route("/accept", api.accept),
            Route("/ip", api.ip),
            Route("/ua", api.user_agent, methods=["GET", "POST"]),
            Route("/user-agent", api.user_agent, methods=["GET", "POST"]),
        ],
    ),
)

app = Starlette(routes=routes)

if __name__ == "__main__":
    from uvicorn import run

    run("main:app", server_header=False, date_header=False)
