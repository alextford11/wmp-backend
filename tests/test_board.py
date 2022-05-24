from tests.conftest import create_basic_board_workout, create_board_workout, create_muscle, create_workout


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
                'sets_value': 3,
                'reps_value': 10,
                'measurement_value': 10,
                'measurement_unit': 'kg',
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
                'sets_value': 3,
                'reps_value': 10,
                'measurement_value': 10,
                'measurement_unit': 'kg',
            },
            {
                'id': board_workout2.id,
                'sort_value': 2,
                'workout': {
                    'id': workout2.id,
                    'related_muscles': [{'id': muscle1.id, 'name': 'Bicep'}, {'id': muscle2.id, 'name': 'Chest'}],
                    'name': 'Push Up',
                },
                'sets_value': 3,
                'reps_value': 10,
                'measurement_value': 10,
                'measurement_unit': 'kg',
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
    r = client.post('/board/9999/update_order/', json={'workout_order': [bw1.id]})
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

    r = client.post(f'/board/{board.id}/workout/', json={'workout_id': workout.id})
    assert r.status_code == 200

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == [
        {
            'id': 1,
            'sort_value': 1,
            'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []},
            'sets_value': 3,
            'reps_value': 10,
            'measurement_value': 10,
            'measurement_unit': 'kg',
        },
    ]


def test_add_workout_to_board_404(db, client, board):
    workout = create_workout(db, name='Push Up')
    r = client.post('/board/9999/workout/', json={'workout_id': workout.id})
    assert r.status_code == 404


def test_add_workout_to_board_no_workouts_exist(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.post(f'/board/{board.id}/workout/')
    assert r.status_code == 422

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_add_workout_to_board_workout_doesnt_exist(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.post(f'/board/{board.id}/workout/', json={'workout_id': 9999})
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
        {
            'id': bw.id,
            'sort_value': 1,
            'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []},
            'sets_value': 3,
            'reps_value': 10,
            'measurement_value': 10,
            'measurement_unit': 'kg',
        }
    ]

    r = client.delete(f'/board/{board.id}/workout/{workout.id}/', json={'board_workout_id': bw.id})
    assert r.status_code == 200

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_remove_workout_from_board_404(db, client, board):
    bw = create_basic_board_workout(db, board=board)
    r = client.delete(f'/board/9999/workout/{bw.id}/', json={'board_workout_id': bw.id})
    assert r.status_code == 404


def test_remove_workout_from_board_workout_doesnt_exist(db, client, board):
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.delete(f'/board/{board.id}/workout/9999/')
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
        {
            'id': bw1.id,
            'sort_value': 1,
            'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []},
            'sets_value': 3,
            'reps_value': 10,
            'measurement_value': 10,
            'measurement_unit': 'kg',
        },
        {
            'id': bw2.id,
            'sort_value': 2,
            'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []},
            'sets_value': 3,
            'reps_value': 10,
            'measurement_value': 10,
            'measurement_unit': 'kg',
        },
    ]

    r = client.delete(f'/board/{board.id}/workout/{bw1.id}/')
    assert r.status_code == 200

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == [
        {
            'id': bw2.id,
            'sort_value': 2,
            'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []},
            'sets_value': 3,
            'reps_value': 10,
            'measurement_value': 10,
            'measurement_unit': 'kg',
        }
    ]


def test_update_board_workout_values(db, client, board):
    workout = create_workout(db, name='Push Up')
    bw = create_board_workout(db, board_id=board.id, workout_id=workout.id)
    r = client.put(f'/board/{board.id}/workout/{bw.id}/', json={'sets_value': 5, 'reps_value': 20})
    assert r.status_code == 200

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == [
        {
            'id': bw.id,
            'sort_value': 1,
            'workout': {'id': workout.id, 'name': 'Push Up', 'related_muscles': []},
            'sets_value': 5,
            'reps_value': 20,
            'measurement_value': 10,
            'measurement_unit': 'kg',
        }
    ]


def test_update_board_workout_values_404(db, client, board):
    r = client.put('/board/9999/workout/9999/', json={'sets_value': 5, 'reps_value': 20})
    assert r.status_code == 404

    r = client.put(f'/board/{board.id}/workout/9999/', json={'sets_value': 5, 'reps_value': 20})
    assert r.status_code == 404


def test_get_measurement_unit_lists(client):
    r = client.get('/board/measurement-units/list/')
    assert r.status_code == 200
    assert r.json() == {
        'options': [
            {'label': 'Kilograms', 'value': 'kg'},
            {'label': 'Grams', 'value': 'g'},
            {'label': 'Pounds', 'value': 'lb'},
            {'label': 'Seconds', 'value': 's'},
            {'label': 'Minutes', 'value': 'min'},
            {'label': 'Hours', 'value': 'h'},
            {'label': 'Calories', 'value': 'cal'},
            {'label': 'Kilometers', 'value': 'km'},
            {'label': 'Meters', 'value': 'm'},
            {'label': 'Centimeters', 'value': 'cm'},
            {'label': 'Miles', 'value': 'mi'},
            {'label': 'Yards', 'value': 'yd'},
            {'label': 'Feet', 'value': 'ft'},
            {'label': 'Inches', 'value': 'in'},
        ]
    }

    r = client.get('/board/measurement-units/categories/')
    assert r.status_code == 200
    assert r.json() == {
        'options': [
            {
                'label': 'Mass',
                'options': [
                    {'label': 'Kilograms', 'value': 'kg'},
                    {'label': 'Grams', 'value': 'g'},
                    {'label': 'Pounds', 'value': 'lb'},
                ],
            },
            {
                'label': 'Time',
                'options': [
                    {'label': 'Seconds', 'value': 's'},
                    {'label': 'Minutes', 'value': 'min'},
                    {'label': 'Hours', 'value': 'h'},
                ],
            },
            {'label': 'Energy', 'options': [{'label': 'Calories', 'value': 'cal'}]},
            {
                'label': 'Length',
                'options': [
                    {'label': 'Kilometers', 'value': 'km'},
                    {'label': 'Meters', 'value': 'm'},
                    {'label': 'Centimeters', 'value': 'cm'},
                    {'label': 'Miles', 'value': 'mi'},
                    {'label': 'Yards', 'value': 'yd'},
                    {'label': 'Feet', 'value': 'ft'},
                    {'label': 'Inches', 'value': 'in'},
                ],
            },
        ]
    }
