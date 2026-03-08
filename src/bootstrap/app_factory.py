import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from domain.errors import DomainError
from presentation.rest.error_handler import domain_error_handler, unexpected_error_handler
from presentation.rest.middlewares import RequestLoggingMiddleware
from bootstrap.ioc import AppProvider, DBProvider, RepositoryProvider, HandlerProvider
from bootstrap.logging_config import setup_logging, log_run_app
from presentation.rest.routers.customer_router import customer_router


def create_app() -> FastAPI:
    setup_logging()
    log_run_app()

    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    app.include_router(customer_router)

    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)

    ioc = make_async_container(
        DBProvider(),
        RepositoryProvider(),
        HandlerProvider(),
        AppProvider()
    )
    setup_dishka(ioc, app)
    return app

if __name__ == "__main__":
    uvicorn.run(
        app=create_app(),
        host="127.0.0.1",
        port=8000,
        access_log=False # We use custom logs
    )
