from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import auth, user
from app.utils.firebase import init_firebase
from app.middlewares.log import LogMiddleware
from app.exceptions.log import LogError
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

global_prefix = "/api/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_firebase()    
    yield


app = FastAPI(lifespan=lifespan)
log = LogError()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogMiddleware)
app.add_exception_handler(RequestValidationError, log.request_validation_exception_handler)
app.add_exception_handler(HTTPException, log.http_exception_handler)
app.add_exception_handler(Exception, log.unhandled_exception_handler)

app.include_router(auth.router, tags=["Auth"], prefix=f"{global_prefix}/auth")
app.include_router(user.router, tags=["User"], prefix=f"{global_prefix}/user")

@app.get("/")
async def root():
    return {"message": "Hello World"}