def test_login_incorrect_data(client):
    r = client.post('/login/', data={'username': 'testing@example.com'})
    assert r.status_code == 422
    assert r.json() == {
        'detail': [{'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}]
    }


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


def test_signup_no_data_posted(client):
    r = client.post('/signup/')
    assert r.status_code == 422
    assert r.json() == {'detail': [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}


def test_signup_create_user_access_token_returned(client):
    r = client.post(
        '/signup/',
        json={'first_name': 'John', 'last_name': 'Smith', 'email': 'testing@example.com', 'password': 'Testing123'},
    )
    assert r.status_code == 200
    assert len(r.json()['access_token']) == 143
    assert r.json()['token_type'] == 'bearer'


def test_signup_user_already_exists(client, user):
    r = client.post(
        '/signup/',
        json={'first_name': 'John', 'last_name': 'Smith', 'email': 'testing@example.com', 'password': 'Testing123'},
    )
    assert r.status_code == 400
    assert r.json() == {'detail': 'User with this email already exists'}


def test_signup_user_password_validation(client):
    data = {'first_name': 'John', 'last_name': 'Smith', 'email': 'testing@example.com', 'password': 'testing'}
    r = client.post('/signup/', json=data)
    assert r.status_code == 422
    assert r.json() == {
        'detail': [
            {
                'loc': ['body', 'password'],
                'msg': 'Password must be longer than 8 characters.',
                'type': 'value_error.passwordvalidation',
            }
        ]
    }

    data['password'] = 'testing='
    r = client.post('/signup/', json=data)
    assert r.status_code == 422
    assert r.json() == {
        'detail': [
            {
                'loc': ['body', 'password'],
                'msg': 'Password contains some invalid characters.',
                'type': 'value_error.passwordvalidation',
            }
        ]
    }

    data['password'] = 'testingpassword'
    r = client.post('/signup/', json=data)
    assert r.status_code == 422
    assert r.json() == {
        'detail': [
            {
                'loc': ['body', 'password'],
                'msg': 'Password must contain at least one number.',
                'type': 'value_error.passwordvalidation',
            }
        ]
    }

    data['password'] = 'testing123'
    r = client.post('/signup/', json=data)
    assert r.status_code == 422
    assert r.json() == {
        'detail': [
            {
                'loc': ['body', 'password'],
                'msg': 'Password must contain at least one uppercase character.',
                'type': 'value_error.passwordvalidation',
            }
        ]
    }

    data['password'] = 'TESTING123'
    r = client.post('/signup/', json=data)
    assert r.status_code == 422
    assert r.json() == {
        'detail': [
            {
                'loc': ['body', 'password'],
                'msg': 'Password must contain at least one lowercase character.',
                'type': 'value_error.passwordvalidation',
            }
        ]
    }
