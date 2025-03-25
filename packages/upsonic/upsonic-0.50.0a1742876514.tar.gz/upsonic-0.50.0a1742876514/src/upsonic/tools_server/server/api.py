from fastapi import FastAPI, HTTPException, Request, Response
import asyncio
from functools import wraps
from ...exception import TimeoutException
import inspect
from starlette.responses import JSONResponse
from concurrent.futures import ThreadPoolExecutor
import threading
import time


from fastapi import FastAPI, HTTPException, Request, Response
import asyncio
from functools import wraps
from ...exception import TimeoutException
import inspect
from starlette.responses import JSONResponse
import signal
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = FastAPI()

# Remove the middleware and use exception handlers instead
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logging.error(f"Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# Import the cleanup function from server_utils instead of tools
from .server_utils import cleanup_all_servers

@app.on_event("shutdown")
async def shutdown_event():
    """
    Clean up all server instances when the application shuts down.
    """
    await cleanup_all_servers()


async def timeout_handler(duration: float, coro):
    try:
        return await asyncio.wait_for(coro, timeout=duration)
    except asyncio.TimeoutError:
        raise TimeoutException(f"Operation timed out after {duration} seconds")
def timeout(seconds: float):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeoutException(f"Function timed out after {seconds} seconds")

            # Set the signal handler and a timeout
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(int(seconds))

            try:
                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                return result
            except TimeoutException as e:
                raise HTTPException(
                    status_code=408,
                    detail=str(e)
                )
            finally:
                # Disable the alarm
                signal.alarm(0)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeoutException(f"Function timed out after {seconds} seconds")

            # Set the signal handler and a timeout
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(int(seconds))

            try:
                return func(*args, **kwargs)
            except TimeoutException as e:
                raise HTTPException(
                    status_code=408,
                    detail=str(e)
                )
            finally:
                # Disable the alarm
                signal.alarm(0)

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
    return decorator

@app.get("/status")
async def get_status():
    return {"status": "Server is running"}
