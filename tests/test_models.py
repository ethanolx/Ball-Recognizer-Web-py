from time import time
import pytest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from application.models.history import History
from application.models.user import User
from application.models.ball import Ball
import re

# Ball Class Validation


@pytest.mark.parametrize('sample', [
    'Basketball',
    'Soccer ball'
])
def test_Ball_Class(sample, capsys):
    with capsys.disabled():
        assert type(sample) is str
        assert sample != ''
        assert Ball(ball_type=sample).ball_type == sample


@pytest.mark.xfail(strict=True, reason='Null Entries')
@pytest.mark.parametrize('sample', [
    None,
    ''
])
def test_Ball_Class_Nulls(sample, capsys):
    test_Ball_Class(sample=sample, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize('sample', [
    123,
    True,
    0.50
])
def test_Ball_Class_Invalid(sample, capsys):
    test_Ball_Class(sample=sample, capsys=capsys)


# User Class Validation
def validate_password(password):
    assert len(password) >= 8, 'Password must contain at least 8 characters'
    assert re.match(
        '.*[A-Z]+.*', password), 'Password must contain at least one uppercase letter'
    assert re.match(
        '.*[a-z]+.*', password), 'Password must contain at least one lowercase letter'
    assert re.match(
        '.*[0-9]+.*', password), 'Password must contain at least one number'
    assert re.match(
        '.*[!@#$%^&*]+.*', password), 'Password must contain at least one special character [!@#$%^&*]'


@pytest.mark.parametrize("sample_list", [
    ['abc@xyz.net', 'John Smith', '12345!@#Xu'],
    ['zyx@abc.net', 'Jane Doe', 'ABCde1#$%']
])
def test_User_Class(sample_list, capsys):
    with capsys.disabled():
        new_user = User(
            email=sample_list[0],
            username=sample_list[1],
            password=generate_password_hash(sample_list[2], method='sha256')
        )

        assert new_user.email == sample_list[0]
        assert new_user.username == sample_list[1]
        validate_password(sample_list[2])
        assert check_password_hash(new_user.password, sample_list[2])


@pytest.mark.xfail(strict=True, reason='Null Entries')
@pytest.mark.parametrize("sample_list", [
    ['aim@arg.org', '', '12345!@#Xu'],
    ['aim@arg.org', 'someone', ''],
    ['', 'someone', '12345!@#Xu'],
    ['aim@arg.org', None, '12345!@#Xu'],
    ['aim@arg.org', 'someone', None],
    [None, 'someone', '12345!@#Xu']
])
def test_User_Class_Nulls(sample_list, capsys):
    test_User_Class(sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize("sample_list", [
    ['abcdefgh', 'Another John', '12345!@#Xu'],
    ['email2@xyz.net', 'John Smith', '12345'],
    ['zyx@abc.net', 'Jane Doe', 'Abcde123']
])
def test_User_Class_Invalid(sample_list, capsys):
    test_User_Class(sample_list=sample_list, capsys=capsys)


def get_current_timestamp():
    return int(time() * 1000.)


def get_current_datetime():
    return datetime.utcnow()


# History Class Validation
@pytest.mark.parametrize('sample_list', [
    [1, 1, 2, 0.45],
    [5, 2, 5, 0.99],
    [10, 3, 7, 0.1],
    [100, 4, 12, 0.24]
])
def test_History_Class(sample_list, capsys):
    with capsys.disabled():
        current_timestamp = get_current_timestamp()
        current_datetime = get_current_datetime()

        test_record = History(
            id=sample_list[0],
            userid=sample_list[1],
            filepath=f'{current_timestamp}.png',
            prediction=sample_list[2],
            probability=sample_list[3],
            uploaded_on=current_datetime
        )

        assert test_record.id == sample_list[0]
        assert test_record.userid == sample_list[1]
        assert test_record.prediction == sample_list[2]
        assert test_record.probability == sample_list[3]

        assert test_record.filepath == f'{current_timestamp}.png'
        assert test_record.uploaded_on == current_datetime


@pytest.mark.xfail(strict=True, reason='Null Entries')
@pytest.mark.parametrize('sample_list', [
    [1, None, 2, 0.45],
    [5, 2, 5, None],
    [100, 4, None, 0.24]
])
def test_History_Class_Nulls(sample_list, capsys):
    test_History_Class(sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Invalid Entries')
@pytest.mark.parametrize('sample_list', [
    ['', 1, 2, 0.45],
    [5, True, 5, 0.99],
    [10, 3, 3.33, 0.1],
    [100, 4, 12, '0.89']
])
def test_History_Class_Invalid(sample_list, capsys):
    test_History_Class(sample_list=sample_list, capsys=capsys)


@pytest.mark.xfail(strict=True, reason='Out of Range')
@pytest.mark.parametrize('sample_list', [
    [1, 1, 0, 0.45],
    [5, 2, -1, 0.99],
    [10, 3, 7, -1],
    [100, 4, 14, 0.24],
    [100, 4, 12, 0],
    [100, 4, 12, 1.]
])
def test_History_Class_Out_Of_Range(sample_list, capsys):
    test_History_Class(sample_list=sample_list, capsys=capsys)
