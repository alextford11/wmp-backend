from src.models import BoardWorkout, Muscle, Workout


def test_create_board(db, client):
    r = client.post('/board/create/')
    assert r.status_code == 200
    assert r.json() == {'board_workouts': [], 'board_workout_order': [], 'id': 1}


def test_get_board(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json() == {'board_workouts': [], 'board_workout_order': [], 'id': board.id}


def test_get_board_with_workouts(db, client, board):
    muscle = Muscle.manager(db).create(Muscle(name='Bicep'))
    workout = Workout(name='Pull Up')
    workout.related_muscles.append(muscle)
    workout = Workout.manager(db).create(workout)
    board_workout = BoardWorkout.manager(db).create(BoardWorkout(board_id=board.id, workout_id=workout.id))
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json() == {
        'board_workouts': [
            {
                'id': board_workout.id,
                'sort_value': 1,
                'workout': {
                    'id': workout.id,
                    'related_muscles': [{'id': muscle.id, 'name': 'Bicep'}],
                    'name': 'Pull Up',
                },
            }
        ],
        'board_workout_order': [board_workout.id],
        'id': board.id,
    }
