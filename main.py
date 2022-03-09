from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.database import Base, get_engine
from src.views import boards, index, workouts

Base.metadata.create_all(bind=get_engine())
ORIGINS = [
    "http://localhost:3000",
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
