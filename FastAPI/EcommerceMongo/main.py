from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from db.connection import db
from routes.product import router as product_router
from routes.category import router as category_router
from routes.cart import router as cart_router
from routes.order import router as order_router
from routes.auth      import router as auth_router
from core.responses   import Success, Error
app=FastAPI()
app.include_router(product_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(auth_router)
# 1. HTTPException handler
@app.exception_handler(StarletteHTTPException)
async def http_exc_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=Error(error=str(exc.detail)).dict()
    )

# 2. Validation errors
@app.exception_handler(RequestValidationError)
async def validation_exc_handler(request: Request, exc: RequestValidationError):
    # Join multiple errors into one string
    msg = "; ".join(f"{e['loc'][-1]}: {e['msg']}" for e in exc.errors())
    return JSONResponse(status_code=422, content=Error(error=msg).dict())

# 3. Generic
@app.exception_handler(Exception)
async def generic_exc_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=Error(error="Internal Server Error").dict())

@app.get("/ping", response_model=Success)
def ping():
    rec = app.state.db.ping_test.find_one({}, {"_id":0,"message":1})
    return Success(data={"message_from_db": rec["message"]})