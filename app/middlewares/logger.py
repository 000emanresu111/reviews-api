from fastapi import Request
from fastapi.logger import logger as fastapi_logger


class LoggerMiddleware:
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        self.log_request(request, response)
        return response

    def log_request(self, request: Request, response):
        fastapi_logger.info(
            "Request - Method: %s, Path: %s, Status: %s",
            request.method,
            request.url.path,
            response.status_code,
        )
