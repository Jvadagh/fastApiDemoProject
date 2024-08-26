# main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from Demo.api.router.authentication_router import authentication_router
from Demo.api.router.demo_router import demo_router

app = FastAPI()

app.include_router(demo_router)
app.include_router(authentication_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
