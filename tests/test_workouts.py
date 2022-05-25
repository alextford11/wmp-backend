def test_workout_list_no_workouts_exist(client):
    r = client.get('/workouts/list/')
    assert r.status_code == 200
    assert r.json() == {'workouts': []}


def test_workout_list_workouts_exist(client, factory):
    m1 = factory.create_muscle(name='Bicep')
    m2 = factory.create_muscle(name='Chest')
    m3 = factory.create_muscle(name='Lats')
    m4 = factory.create_muscle(name='Triceps')
    m5 = factory.create_muscle(name='Shoulders')

    w1 = factory.create_workout(name='Push Up', muscles=[m1, m2])
    w2 = factory.create_workout(name='Pull Up', muscles=[m2, m3])
    w3 = factory.create_workout(name='Preacher Curl', muscles=[m3, m4])
    w4 = factory.create_workout(name='Bench Press', muscles=[m4, m5])
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


def test_workout_list_grouped(client, factory):
    m1 = factory.create_muscle(name='Bicep')
    m2 = factory.create_muscle(name='Chest')
    m3 = factory.create_muscle(name='Lats')
    m4 = factory.create_muscle(name='Triceps')
    m5 = factory.create_muscle(name='Shoulders')

    w1 = factory.create_workout(name='Push Up', muscles=[m1, m2])
    w2 = factory.create_workout(name='Pull Up', muscles=[m2, m3])
    w3 = factory.create_workout(name='Preacher Curl', muscles=[m3, m4])
    w4 = factory.create_workout(name='Bench Press', muscles=[m4, m5])
    r = client.get('/workouts/list/grouped/')
    assert r.status_code == 200
    assert r.json() == {
        'options': [
            {'label': 'Bicep', 'options': [{'value': str(w1.id), 'label': 'Push Up'}]},
            {
                'label': 'Chest',
                'options': [
                    {'value': str(w2.id), 'label': 'Pull Up'},
                    {'value': str(w1.id), 'label': 'Push Up'},
                ],
            },
            {
                'label': 'Lats',
                'options': [
                    {'value': str(w3.id), 'label': 'Preacher Curl'},
                    {'value': str(w2.id), 'label': 'Pull Up'},
                ],
            },
            {'label': 'Shoulders', 'options': [{'value': str(w4.id), 'label': 'Bench Press'}]},
            {
                'label': 'Triceps',
                'options': [
                    {'value': str(w4.id), 'label': 'Bench Press'},
                    {'value': str(w3.id), 'label': 'Preacher Curl'},
                ],
            },
        ]
    }
