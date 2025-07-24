from fastapi import FastAPI, HTTPException,Request
from db.connection import get_db_connection
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from routes.product import router as product_router
from routes.auth import router as auth_router
from routes.category import router as category_router
from routes.cart import router as cart_router
from routes.order import router as order_router
from routes.auth    import router as auth_router
from  auth.deps     import get_current_active_user
app=FastAPI()

app.include_router(product_router)
app.include_router(category_router)

app.include_router(cart_router)
app.include_router(auth_router)
# Protect orders
app.include_router(order_router, dependencies=[Depends(get_current_active_user)])
app.include_router(order_router)
@app.get("/")
def root():
    return{"message":"Created basic structure successfully"}
# 1. HTTPException handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

# 2. Validation errors (Pydantic)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": exc.errors()}
    )

# 3. Fallback for uncaught exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # In production: log exc
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal Server Error"}
    )

@app.get("/ping")
def ping():
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT message FROM ping_test LIMIT 1;")
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404,detail="No ping record found")
    return {"message_from_db":result["message"]}
