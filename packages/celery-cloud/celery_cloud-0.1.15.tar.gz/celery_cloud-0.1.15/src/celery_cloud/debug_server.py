import debugpy
from fastapi import FastAPI

from .settings import settings

app = FastAPI()

debugpy.listen(("0.0.0.0", settings.SERVER_DEBUG_PORT))
print("Waiting for connection from the debugger...")
debugpy.wait_for_client()


@app.post("/lambda")
async def run_lambda(event: dict):
    from celery_cloud.runner import (
        lambda_handler,
    )  # Import the real function

    response = lambda_handler(event, None)
    return response
