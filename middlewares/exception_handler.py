# middlewares/exception_handler.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from core import get_logger

logger = get_logger(__name__)


"""
FastAPI provides a handy way to handle exceptions across your whole application using middleware. This approach provides a way to catch exceptions and format responses accordingly. It`s also useful for logging and tracking errors.

In this example, we`re catching two types of exceptions:

HTTPException: This is a special type of exception provided by FastAPI that allows you to return HTTP responses with specific status codes and content.

A generic Exception: This is a catch-all for any other type of exception that might be raised. In this case, we`re returning a 500 internal server error response.

The get_logger function from our core package is used to log the details of the exception. We log a different message based on the type of exception to help with debugging.

As for other middlewares, the specific ones you may want to include will largely depend on your application`s needs. Some examples might include middlewares for handling authentication, headers, CORS, etc.
"""

async def exception_handler_middleware(request: Request, call_next):
    """
    Middleware for handling exceptions.
    Catch all exceptions and return a formatted JSON response.
    Also, log the error for debugging purposes.
    """
    try:
        return await call_next(request)
    except HTTPException as e:
        logger.error(f"An error occurred: {e.detail}")
        return JSONResponse(
            status_code=e.status_code,
            content={"message": e.detail},
        )
    except Exception as e:
        logger.error(f"An internal error occurred: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"},
        )

# You can add other known exceptions and how you want to handle them below...
