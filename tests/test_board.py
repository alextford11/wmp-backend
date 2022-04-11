from tests.conftest import create_muscle, create_workout, create_board_workout, create_basic_board_workout


def test_create_board(db, client):
    r = client.post('/board/create/')
    assert r.status_code == 200
    assert r.json() == {'board_workouts': [], 'board_workout_order': [], 'board_muscle_counts': {}, 'id': 1}


def test_get_board(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json() == {'board_workouts': [], 'board_workout_order': [], 'board_muscle_counts': {}, 'id': board.id}


def test_get_board_404(db, client, board):
    r = client.get('/board/9999/')
    assert r.status_code == 404


def test_get_board_with_workouts(db, client, board):
    muscle = create_muscle(db, name='Bicep')
    workout = create_workout(db, name='Pull Up', muscles=[muscle])
    board_workout = create_board_workout(db, board_id=board.id, workout_id=workout.id)
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
        'board_muscle_counts': {'Bicep': 1},
        'id': board.id,
    }


def test_get_board_with_multiple_workouts(db, client, board):
    muscle1 = create_muscle(db, name='Bicep')
    muscle2 = create_muscle(db, name='Chest')

    workout1 = create_workout(db, name='Pull Up', muscles=[muscle1])
    board_workout1 = create_board_workout(db, board_id=board.id, workout_id=workout1.id)

    workout2 = create_workout(db, name='Push Up', muscles=[muscle1, muscle2])
    board_workout2 = create_board_workout(db, board_id=board.id, workout_id=workout2.id)
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json() == {
        'board_workouts': [
            {
                'id': board_workout1.id,
                'sort_value': 1,
                'workout': {
                    'id': workout1.id,
                    'related_muscles': [{'id': muscle1.id, 'name': 'Bicep'}],
                    'name': 'Pull Up',
                },
            },
            {
                'id': board_workout2.id,
                'sort_value': 2,
                'workout': {
                    'id': workout2.id,
                    'related_muscles': [{'id': muscle1.id, 'name': 'Bicep'}, {'id': muscle2.id, 'name': 'Chest'}],
                    'name': 'Push Up',
                },
            },
        ],
        'board_workout_order': [board_workout1.id, board_workout2.id],
        'board_muscle_counts': {'Bicep': 2, 'Chest': 1},
        'id': board.id,
    }


def test_update_workout_order(db, client, board):
    bw1 = create_basic_board_workout(db, board)
    bw2 = create_basic_board_workout(db, board)
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workout_order'] == [bw1.id, bw2.id]

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [bw2.id, bw1.id]})
    assert r.status_code == 200

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workout_order'] == [bw2.id, bw1.id]


def test_update_workout_404(db, client, board):
    bw1 = create_basic_board_workout(db, board)
    r = client.post(f'/board/9999/update_order/', json={'workout_order': [bw1.id]})
    assert r.status_code == 404


def test_update_workout_order_no_workouts(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.json()['board_workout_order'] == []

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': []})
    assert r.status_code == 200

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [1]})
    assert r.status_code == 400, r.json()


def test_update_workout_order_1_workout(db, client, board):
    bw1 = create_basic_board_workout(db, board)
    r = client.get(f'/board/{board.id}/')
    assert r.json()['board_workout_order'] == [bw1.id]

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': []})
    assert r.status_code == 400

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [bw1.id, 2]})
    assert r.status_code == 400

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [bw1.id, bw1.id]})
    assert r.status_code == 200


def test_update_workout_order_multiple_workout(db, client, board):
    bw1 = create_basic_board_workout(db, board)
    bw2 = create_basic_board_workout(db, board)
    bw3 = create_basic_board_workout(db, board)
    r = client.get(f'/board/{board.id}/')
    assert r.json()['board_workout_order'] == [bw1.id, bw2.id, bw3.id]

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': []})
    assert r.status_code == 400

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [bw1.id, bw2.id, bw3.id]})
    assert r.status_code == 200

    r = client.post(
        f'/board/{board.id}/update_order/', json={'workout_order': [bw1.id, bw2.id, bw3.id, bw1.id, bw2.id, bw3.id]}
    )
    assert r.status_code == 200

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [100, 999, 200]})
    assert r.status_code == 400


def test_add_workout_to_board(db, client, board):
    workout = create_workout(db, name='Push Up')
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.post(f'/board/{board.id}/add_workout/', json={'workout_id': workout.id})
    assert r.status_code == 200

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == [
        {
            'id': 1,
            'sort_value': 1,
            'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []},
        },
    ]


def test_add_workout_to_board_404(db, client, board):
    workout = create_workout(db, name='Push Up')
    r = client.post(f'/board/9999/add_workout/', json={'workout_id': workout.id})
    assert r.status_code == 404


def test_add_workout_to_board_no_workouts_exist(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.post(f'/board/{board.id}/add_workout/')
    assert r.status_code == 422

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_add_workout_to_board_workout_doesnt_exist(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.post(f'/board/{board.id}/add_workout/', json={'workout_id': 9999})
    assert r.status_code == 404

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_remove_workout_from_board(db, client, board):
    workout = create_workout(db, name='Push Up')
    bw = create_board_workout(db, board_id=board.id, workout_id=workout.id)
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == [
        {'id': bw.id, 'sort_value': 1, 'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []}}
    ]

    r = client.post(f'/board/{board.id}/remove_workout/', json={'board_workout_id': bw.id})
    assert r.status_code == 200

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_remove_workout_from_board_404(db, client, board):
    bw = create_basic_board_workout(db, board=board)
    r = client.post(f'/board/9999/remove_workout/', json={'board_workout_id': bw.id})
    assert r.status_code == 404


def test_remove_workout_from_board_no_workouts_exist(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.post(f'/board/{board.id}/remove_workout/')
    assert r.status_code == 422

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_remove_workout_from_board_workout_doesnt_exist(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.post(f'/board/{board.id}/remove_workout/', json={'board_workout_id': 9999})
    assert r.status_code == 404

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_remove_multiple_same_workout_from_board(db, client, board):
    workout = create_workout(db, name='Push Up')
    bw1 = create_board_workout(db, board_id=board.id, workout_id=workout.id)
    bw2 = create_board_workout(db, board_id=board.id, workout_id=workout.id)
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == [
        {'id': bw1.id, 'sort_value': 1, 'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []}},
        {'id': bw2.id, 'sort_value': 2, 'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []}}
    ]

    r = client.post(f'/board/{board.id}/remove_workout/', json={'board_workout_id': bw1.id})
    assert r.status_code == 200

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == [
        {'id': bw2.id, 'sort_value': 2, 'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []}}
    ]
