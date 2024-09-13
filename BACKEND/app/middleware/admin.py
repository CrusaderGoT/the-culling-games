'''for the '''
from ..api.main import app
from fastapi import Request, HTTPException, status
import time


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    t = True
    if t:
        raise HTTPException(609)
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

