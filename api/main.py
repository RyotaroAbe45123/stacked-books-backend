from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import user, stack, book


app = FastAPI()
app.include_router(user.router)
app.include_router(stack.router)
app.include_router(book.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
