from src.models import Board


def test_create_board_no_user(client, db):
    r = client.post('/board/create/', json={'user_access_token': None})
    assert r.status_code == 200, r.json()
    assert r.json() == {'board_workouts': [], 'board_workout_order': [], 'board_muscle_counts': {}, 'id': 1}
    assert not Board.manager(db).get().user_id


def test_create_board_with_user(client, db, user, factory):
    access_token = factory.get_user_access_token(user)
    r = client.post('/board/create/', json={'user_access_token': access_token})
    assert r.status_code == 200
    assert r.json() == {'board_workouts': [], 'board_workout_order': [], 'board_muscle_counts': {}, 'id': 1}
    assert Board.manager(db).get().user_id == user.id


def test_get_board(client, factory):
    board = factory.create_board()
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json() == {'board_workouts': [], 'board_workout_order': [], 'board_muscle_counts': {}, 'id': board.id}


def test_get_board_404(client, factory):
    r = client.get('/board/9999/')
    assert r.status_code == 404


def test_get_board_with_workouts(client, factory):
    board = factory.create_board()
    muscle = factory.create_muscle(name='Bicep')
    workout = factory.create_workout(name='Pull Up', muscles=[muscle])
    board_workout = factory.create_board_workout(board=board, workout=workout)
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


def test_get_board_with_multiple_workouts(client, factory):
    board = factory.create_board()
    muscle1 = factory.create_muscle(name='Bicep')
    muscle2 = factory.create_muscle(name='Chest')

    workout1 = factory.create_workout(name='Pull Up', muscles=[muscle1])
    board_workout1 = factory.create_board_workout(board=board, workout=workout1)

    workout2 = factory.create_workout(name='Push Up', muscles=[muscle1, muscle2])
    board_workout2 = factory.create_board_workout(board=board, workout=workout2)
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


def test_update_workout_order(client, factory):
    board = factory.create_board()
    bw1 = factory.create_board_workout(board=board)
    bw2 = factory.create_board_workout(board=board)
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workout_order'] == [bw1.id, bw2.id]

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [bw2.id, bw1.id]})
    assert r.status_code == 200

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workout_order'] == [bw2.id, bw1.id]


def test_update_workout_404(client, factory):
    board = factory.create_board()
    bw1 = factory.create_board_workout(board=board)
    r = client.post('/board/9999/update_order/', json={'workout_order': [bw1.id]})
    assert r.status_code == 404


def test_update_workout_order_no_workouts(client, factory):
    board = factory.create_board()
    r = client.get(f'/board/{board.id}/')
    assert r.json()['board_workout_order'] == []

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': []})
    assert r.status_code == 200

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [1]})
    assert r.status_code == 400, r.json()


def test_update_workout_order_1_workout(client, factory):
    board = factory.create_board()
    bw1 = factory.create_board_workout(board=board)
    r = client.get(f'/board/{board.id}/')
    assert r.json()['board_workout_order'] == [bw1.id]

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': []})
    assert r.status_code == 400

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [bw1.id, 2]})
    assert r.status_code == 400

    r = client.post(f'/board/{board.id}/update_order/', json={'workout_order': [bw1.id, bw1.id]})
    assert r.status_code == 200


def test_update_workout_order_multiple_workout(client, factory):
    board = factory.create_board()
    bw1 = factory.create_board_workout(board=board)
    bw2 = factory.create_board_workout(board=board)
    bw3 = factory.create_board_workout(board=board)
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


def test_add_workout_to_board(client, factory):
    board = factory.create_board()
    workout = factory.create_workout(name='Push Up')
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


def test_add_workout_to_board_404(client, factory):
    factory.create_board()
    workout = factory.create_workout(name='Push Up')
    r = client.post('/board/9999/workout/', json={'workout_id': workout.id})
    assert r.status_code == 404


def test_add_workout_to_board_no_workouts_exist(client, factory):
    board = factory.create_board()
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.post(f'/board/{board.id}/workout/')
    assert r.status_code == 422

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_add_workout_to_board_workout_doesnt_exist(client, factory):
    board = factory.create_board()
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.post(f'/board/{board.id}/workout/', json={'workout_id': 9999})
    assert r.status_code == 404

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_remove_workout_from_board(client, factory):
    board = factory.create_board()
    workout = factory.create_workout(name='Push Up')
    bw = factory.create_board_workout(board=board, workout=workout)
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


def test_remove_workout_from_board_404(client, factory):
    board = factory.create_board()
    bw = factory.create_board_workout(board=board)
    r = client.delete(f'/board/9999/workout/{bw.id}/', json={'board_workout_id': bw.id})
    assert r.status_code == 404


def test_remove_workout_from_board_workout_doesnt_exist(client, factory):
    board = factory.create_board()
    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []

    r = client.delete(f'/board/{board.id}/workout/9999/')
    assert r.status_code == 404

    r = client.get(f'/board/{board.id}/')
    assert r.status_code == 200
    assert r.json()['board_workouts'] == []


def test_remove_multiple_same_workout_from_board(client, factory):
    board = factory.create_board()
    workout = factory.create_workout(name='Push Up')
    bw1 = factory.create_board_workout(board=board, workout=workout)
    bw2 = factory.create_board_workout(board=board, workout=workout)
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


def test_update_board_workout_values(client, factory):
    board = factory.create_board()
    workout = factory.create_workout(name='Push Up')
    bw = factory.create_board_workout(board=board, workout=workout)
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


def test_update_board_workout_values_404(client, factory):
    board = factory.create_board()
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


def test_board_list_view_for_user(client, factory, user):
    user_access_token = factory.get_user_access_token(user)
    board = factory.create_board(user_id=user.id)
    workout = factory.create_workout()
    bw = factory.create_board_workout(board=board, workout=workout)
    r = client.get('/user/boards/', headers={'Authorization': 'Bearer ' + user_access_token})
    assert r.status_code == 200
    assert r.json() == {
        'boards': [
            {
                'id': board.id,
                'board_workouts': [
                    {
                        'id': bw.id,
                        'sort_value': 1,
                        'workout': {'id': workout.id, 'name': 'Bench Press', 'related_muscles': []},
                        'sets_value': 3,
                        'reps_value': 10,
                        'measurement_value': 10,
                        'measurement_unit': 'kg',
                    }
                ],
                'board_workout_order': [],
                'board_muscle_counts': {},
            }
        ]
    }
