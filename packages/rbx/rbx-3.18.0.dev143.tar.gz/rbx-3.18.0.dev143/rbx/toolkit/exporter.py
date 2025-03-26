import logging

from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import Response
from starlette.routing import Route

from . import Options, run

config = Config()
logging.basicConfig(level=config("LOG_LEVEL", default="INFO"))


async def handler(request):
    payload = await request.json()

    filename = None
    name = payload.get("name")
    if name:
        ext = "mp4" if payload["format"] == "video" else "png"
        filename = f"{name}.{ext}"

    project_id = config("GOOGLE_CLOUD_PROJECT", default="dev-platform-eu")

    await run(
        options=Options(
            url=payload["url"],
            width=payload["width"],
            height=payload["height"],
            format=payload["format"],
            duration=int(payload.get("duration", 0)),
            output=f"gs://{project_id}.appspot.com/toolkit/exports/",
            filename=filename,
        )
    )

    return Response("OK")


def create_app() -> Starlette:
    return Starlette(
        routes=[
            Route("/", endpoint=handler, methods=["POST"]),
        ]
    )
