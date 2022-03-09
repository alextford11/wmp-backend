from tests.conftest import create_workout, create_muscle


def test_workout_list_no_workouts_exist(db, client):
    r = client.get('/workouts/list/')
    assert r.status_code == 200
    assert r.json() == {'workouts': []}


def test_workout_list_workouts_exist(db, client):
    m1 = create_muscle(db, name='Bicep')
    m2 = create_muscle(db, name='Chest')
    m3 = create_muscle(db, name='Lats')
    m4 = create_muscle(db, name='Triceps')
    m5 = create_muscle(db, name='Shoulders')

    w1 = create_workout(db, name='Push Up', muscles=[m1, m2])
    w2 = create_workout(db, name='Pull Up', muscles=[m2, m3])
    w3 = create_workout(db, name='Preacher Curl', muscles=[m3, m4])
    w4 = create_workout(db, name='Bench Press', muscles=[m4, m5])
    r = client.get('/workouts/list/')
    assert r.status_code == 200
    assert r.json() == {
        'workouts': [
            {
                'id': w1.id,
                'name': 'Push Up',
                'related_muscles': [{'id': m1.id, 'name': 'Bicep'}, {'id': m2.id, 'name': 'Chest'}],
            },
            {
                'id': w2.id,
                'name': 'Pull Up',
                'related_muscles': [{'id': m2.id, 'name': 'Chest'}, {'id': m3.id, 'name': 'Lats'}],
            },
            {
                'id': w3.id,
                'name': 'Preacher Curl',
                'related_muscles': [{'id': m3.id, 'name': 'Lats'}, {'id': m4.id, 'name': 'Triceps'}],
            },
            {
                'id': w4.id,
                'name': 'Bench Press',
                'related_muscles': [{'id': m4.id, 'name': 'Triceps'}, {'id': m5.id, 'name': 'Shoulders'}],
            },
        ]
    }
