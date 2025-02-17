from fastapi import FastAPI

from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import JSONResponse

# from JustForLearning import response_model_examples, learning
import security
import items
import users

app = FastAPI()

app.include_router(items.router)
# app.include_router(response_model_examples.router)
app.include_router(security.router)
app.include_router(users.router)
# app.include_router(learning.router)


@app.get("/")
async def root():
    return {"message": "Welcome to LOL items API"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.exception_handler(SQLAlchemyError)
async def sql_alchemy_error_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"message": f"{exc}"},
    )