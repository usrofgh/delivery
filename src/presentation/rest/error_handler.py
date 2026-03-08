from starlette.requests import Request
from starlette.responses import JSONResponse

from domain.errors import DomainError, ErrorCodes as Ec
from bootstrap.logging_config import log_domain_error, log_unexpected_error

_HTTP_CODE_MAPPER: dict[str, int] = {
    Ec.INVALID_UUID_VALUE: 400,

    Ec.INVALID_BUSINESS_TAX_NUMBER: 400,

    Ec.INVALID_EMAIL: 400,
    Ec.EMAIL_ALREADY_EXISTS: 409,

    Ec.INVALID_PRICE: 400,
    Ec.INVALID_DAY_OF_WEEK: 400,
    Ec.INVALID_WORK_HOURS: 400,
    Ec.INVALID_INVENTORY_TYPE: 400,
    Ec.INVALID_ORDER_STATUS_TRANSITION: 400,
    Ec.INVALID_PASSWORD_FORMAT: 400,
}


async def domain_error_handler(request: Request, error: DomainError) -> JSONResponse:
    error_code = error.args[0]
    status_code = _HTTP_CODE_MAPPER.get(error_code, 400)
    log_domain_error(path=request.url.path, error_code=error_code, status_code=status_code)
    return JSONResponse(
        status_code=status_code,
        content={"error": {"error_code": error_code}}
    )


async def unexpected_error_handler(request: Request, error: Exception) -> JSONResponse:
    log_unexpected_error(path=request.url.path, exc_info=error)
    return JSONResponse(
        status_code=500,
        content={"error": {"error_code": "DOMAIN_ERROR"}}
    )
