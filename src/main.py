from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/board')
async def get_board():
    return {
        'board': {
            'workouts': {
                'workout-1': {
                    'id': 'workout-1',
                    'title': 'Push Up',
                    'muscles': {
                        'muscle-2': {
                            'id': 'muscle-2',
                            'name': 'Chest',
                        },
                        'muscle-3': {
                            'id': 'muscle-3',
                            'name': 'Biceps',
                        },
                    },
                },
                'workout-2': {
                    'id': 'workout-2',
                    'title': 'High Cable Fly',
                    'muscles': {
                        'muscle-1': {
                            'id': 'muscle-1',
                            'name': 'Shoulders',
                        },
                        'muscle-2': {
                            'id': 'muscle-2',
                            'name': 'Chest',
                        },
                        'muscle-3': {
                            'id': 'muscle-3',
                            'name': 'Triceps',
                        },
                    },
                },
            },
            'workout_order': ['workout-1', 'workout-2'],
        }
    }
