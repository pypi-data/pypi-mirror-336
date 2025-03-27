import os
import sys

from eventix.functions.eventix_client import EventixClient

try:
    import fastapi
    from fastapi import APIRouter, Body
    from fastapi import Request, Response

except:
    pass


def fastapi_eventix_router_wrapper(self):
    if 'fastapi' not in sys.modules:  # pragma: no cover
        raise Exception('fastapi not installed but required by fastapi_eventix_router_wrapper')

    eventix_router = APIRouter(prefix="", tags=["eventix"])
    @eventix_router.get("/task/by_unique_key/{unique_key}")
    def router_task_by_unique_key_for_namespace_get(unique_key: str):
        namespace = os.environ.get("EVENTIX_NAMESPACE", None)
        r= EventixClient.get_task_by_unique_key_and_namespace(unique_key,namespace=namespace)
        return r.json()
    self.include_router(eventix_router)
