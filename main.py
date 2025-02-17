import logging
from fastapi import FastAPI

import exception_handlers
# from JustForLearning import response_model_examples, learning
import security
import items
import users

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, filename="app.log", format="%(asctime)s - %(levelname)s - %(message)s")
# Register exception handlers (Call the registration function)
exception_handlers.register_exception_handlers(app)

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
