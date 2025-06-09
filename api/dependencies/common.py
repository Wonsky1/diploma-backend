from typing import Annotated
from fastapi import Request, Depends
import uuid


def get_request_id(request: Request) -> str:
    return request.headers.get("X-Request-Id", str(uuid.uuid4()))


RequestIdDep = Annotated[str, Depends(get_request_id)]
