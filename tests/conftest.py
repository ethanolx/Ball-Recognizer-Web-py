import os
import shutil
import pathlib
from flask import request
import pytest
from application import create_app

test_app = create_app(env='testing')


@pytest.fixture
def app():
    with test_app.app_context():
        yield test_app


@pytest.fixture
def url():
    with test_app.app_context():
        return request.url_root


@pytest.fixture
def client(app):
    return app.test_client()


def garbage_collection():
    shutil.rmtree('tests/tmp', ignore_errors=True)
    os.mkdir('tests/tmp')


garbage_collection()