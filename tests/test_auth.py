def test_login_incorrect_data(client):
    r = client.post('/login/', data={'username': 'testing@example.com'})
    assert r.status_code == 422
    assert (
        r.json()
        == {'detail': [{'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}]}
        != {'detail': 'Incorrect username or password'}
    )


def test_login_no_user_exists(client):
    r = client.post('/login/', data={'username': 'testing@example.com', 'password': 'testing'})
    assert r.status_code == 401
    assert r.json() == {'detail': 'Incorrect username or password'}


def test_login_successful(client, user):
    r = client.post('/login/', data={'username': 'testing@example.com', 'password': 'testing'})
    assert r.status_code == 200
    assert len(r.json()['access_token']) == 143
    assert r.json()['token_type'] == 'bearer'


def test_login_incorrect_password(client, user):
    r = client.post('/login/', data={'username': 'testing@example.com', 'password': 'testing123'})
    assert r.status_code == 401
    assert r.json() == {'detail': 'Incorrect username or password'}


def test_login_incorrect_email(client, user):
    r = client.post('/login/', data={'username': 'testing123@example.com', 'password': 'testing'})
    assert r.status_code == 401
    assert r.json() == {'detail': 'Incorrect username or password'}


def test_access_code(client, user):
    r = client.post('/login/', data={'username': 'testing@example.com', 'password': 'testing'})
    assert r.status_code == 200

    access_token = r.json()['access_token']
    r = client.get('/user/profile/', headers={'Authorization': f'Bearer {access_token}'})
    assert r.status_code == 200
    assert r.json() == {
        'id': user.id,
        'email': 'testing@example.com',
        'first_name': 'Billy',
        'last_name': 'Holiday',
    }


def test_access_code_incorrect(client):
    r = client.get('/user/profile/', headers={'Authorization': 'Bearer something incorrect'})
    assert r.status_code == 401
    assert r.json() == {'detail': 'Could not validate credentials'}
