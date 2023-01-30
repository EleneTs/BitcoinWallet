from typing import Any

from starlette.requests import Request


def get_core(request: Request) -> Any:
    return request.app.state.core
