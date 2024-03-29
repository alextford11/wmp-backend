from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.database import Base, get_engine
from src.views import boards, index, workouts, users, auth

Base.metadata.create_all(bind=get_engine())
ORIGINS = [
    'http://localhost:3000',
    'https://frontend-wmp.herokuapp.com',
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(boards.router)
app.include_router(index.router)
app.include_router(workouts.router)
app.include_router(users.router)
app.include_router(auth.router)
