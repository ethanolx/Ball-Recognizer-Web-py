import json
import pytest
from datetime import datetime
from werkzeug.security import check_password_hash
from application import DATETIME_FORMAT
from email_validator import validate_email
from tests.test_models import test_History_Class


# New User API
@pytest.mark.parametrize('sample_list', [
    ['ethan@gmail.com', 'Ethan', '12345Abc#'],
    ['john@abc.net', 'Doe', '12345^32Jm'],
    ['jane@abc.net', 'J', '12345^32Jm'],
    ['joe@abc.net', 'Joe', '12345^32Jm']
])
def test_add_new_user_api(client, sample_list, capsys):
    with capsys.disabled():
        for field in sample_list:
            assert type(field) is str
            assert field != ''
        assert validate_email(sample_list[0])

        data = {
            'email': sample_list[0],
            'new_username': sample_list[1],
            'new_password': sample_list[2],
            'confirm_password': sample_list[2],
        }
        response = client.post('/auth/sign-up',
                               data=data,
                               content_type='application/x-www-form-urlencoded')

        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/home'


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize('sample_list', [
    ['invalidemail', 'John', '12345Abc#'],
    ['valid@email.org', 127, '12345Abc#'],
    ['valid@email.org', 'Ethan', '1111111']
])
def test_add_new_user_api_invalid(client, sample_list, capsys):
    test_add_new_user_api(client=client, sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Null Entries')
@pytest.mark.parametrize('sample_list', [
    [None, 'John', '12345Abc#', 2],
    ['valid@email.org', None, '12345Abc#', 2],
    ['valid@email.org', 'a user', None, 2]
])
def test_add_new_user_api_nulls(client, sample_list, capsys):
    test_add_new_user_api(
        client=client, sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Duplicate Entries')
@pytest.mark.parametrize('sample_list', [
    ['ethan@gmail.com', 'John', '12345Abc#', 2],
    ['valid@email.org', 'Ethan', '12345Abc#', 2],
    ['valid@email.org', 'Ethan', 'mdqpdl129(20L', 2]
])
def test_add_new_user_api_duplicates(client, sample_list, capsys):
    test_add_new_user_api(
        client=client, sample_list=sample_list, capsys=capsys)


# Get User API
@pytest.mark.parametrize('sample_list', [
    [1, 'ethan@gmail.com', 'Ethan', '12345Abc#'],
    [2, 'john@abc.net', 'Doe', '12345^32Jm'],
    [3, 'jane@abc.net', 'J', '12345^32Jm'],
    [4, 'joe@abc.net', 'Joe', '12345^32Jm']
])
def test_get_user_api(client, sample_list, capsys):
    with capsys.disabled():
        response = client.get(f'/api/user/get/{sample_list[0]}')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'

        user = json.loads(response.get_data(as_text=True))
        assert user['id'] == sample_list[0]
        assert user['email'] == sample_list[1]
        assert user['username'] == sample_list[2]
        assert check_password_hash(user['password'], sample_list[3])


@pytest.mark.xfail(strict=True, reason='Non-existent User')
@pytest.mark.parametrize('sample_list', [
    [5, 'ethan@gmail.com', 'Ethan', '12345Abc#']
])
def test_get_user_api_nulls(client, sample_list, capsys):
    test_get_user_api(client, sample_list, capsys)


# New Prediction API
@pytest.mark.parametrize('sample_list', [
    ['basketball.jpg', 'Basketball', 0.43],
    ['soccer-ball.jpg', 'Soccer ball', 0.77],
    ['tennis-ball.jpg', 'Tennis ball', 0.99],
])
def test_new_prediction_api(client, sample_list):
    with client:
        client.post('/auth/login',
                    data={'username': 'ethan', 'password': '12345Abc#'},
                    content_type='application/x-www-form-urlencoded')

        with open('tests/test_images/' + sample_list[0], 'rb') as img_file:
            data = {
                'image': (img_file, 'image')
            }

            response = client.post('/predict',
                                   data=data,
                                   buffered=True,
                                   content_type='multipart/form-data')

            result = response.json
            assert result['prediction'] == sample_list[1]
            assert result['probability'] >= sample_list[2]


# Get prediction API
@pytest.mark.parametrize('sample', [
    {
        'id': 1,
        'userid': 1,
        'prediction': 2,
        'probability': 0.43
    },
    {
        'id': 2,
        'userid': 1,
        'prediction': 9,
        'probability': 0.77
    },
    {
        'id': 3,
        'userid': 1,
        'prediction': 10,
        'probability': 0.99
    }
])
def test_get_prediction_api(client, sample, capsys):
    with capsys.disabled():
        sample_id = sample['id']
        response = client.get(f'/api/prediction/{sample_id}')
        result = response.json
        epsilon = 0.01

        uploaded_on = datetime.strptime(result['uploaded_on'], DATETIME_FORMAT)
        file_name_stamp = datetime.utcfromtimestamp(int(result['filepath'].replace('.png', '')) // 1000)

        time_diff = uploaded_on - file_name_stamp
        assert time_diff.days == 0
        assert time_diff.seconds > 0

        assert result['id'] == sample['id']
        assert result['userid'] == sample['userid']
        assert result['prediction'] == sample['prediction']
        assert abs(result['probability'] - sample['probability']) < epsilon

        test_History_Class(sample_list=[
            result['id'],
            result['userid'],
            result['prediction'],
            result['probability']
        ], capsys=capsys)


# Delete Prediction API
@pytest.mark.parametrize('sample', [
    1, 2, 3
])
def test_delete_prediction_api(client, sample, capsys):
    with capsys.disabled():
        response = client.post('/remove',
                               data={'id': sample},
                               content_type='application/x-www-form-urlencoded')
        assert response.status_code == 302

        response = client.get(f'/api/prediction/{sample}')
        assert response.json is None
