from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from application.commands.customers.register_customer_handler import RegisterCustomerHandler
from application.commands.customers.verify_register_customer_handler import VerifyRegisterCustomerHandler
from bootstrap.ioc import RepositoryProvider
from infrastracture.db.repositories import customer_repository
from presentation.rest.schemas.customer_schemas import RegisterCustomerSchema, RegisterCustomerResponseSchema, \
    RegisterCustomerConfirmSchema

customer_router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@customer_router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterCustomerResponseSchema
)
@inject
async def register_customer(
        register_schema: RegisterCustomerSchema,
        handler: FromDishka[RegisterCustomerHandler]
):
    await handler(**register_schema.model_dump())
    return RegisterCustomerResponseSchema

@customer_router.get(
    path="/{customer_id}",
    status_code=status.HTTP_200_OK
)
async def get_user(
    repo: FromDishka[customer_repository]
):
    print()

@customer_router.post(
    path="/register/verify",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterCustomerResponseSchema
)
@inject
async def verify(
        verify_schema: RegisterCustomerConfirmSchema,
        handler: FromDishka[VerifyRegisterCustomerHandler]
):
    await handler(**verify_schema.model_dump())
    return RegisterCustomerResponseSchema
