import os
import subprocess
import sys
import pytest


@pytest.mark.parametrize('constraint', [
    '>= 3.7', '< 3.10'
])
def test_python_version(constraint):
    python_version = (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    comparator, version = constraint.split(' ')
    version_tuple = tuple(map(int, version.split('.')))
    assert eval(f'{python_version}{comparator}{version_tuple}')


def test_imports():
    with open('requirements.txt', 'r') as requirements:
        required_libs = requirements.read().splitlines()
        installed_libs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).splitlines()
        for i, required_lib in enumerate(required_libs):
            assert required_lib == installed_libs[i].decode(), f'{required_lib} != {installed_libs[i].decode()}'


def check_files_recursively(file_structure, previous_dirs=[]):
    if type(file_structure) is dict:
        for item, children in file_structure.items():
            current_item = os.path.join(*previous_dirs, item)
            assert os.path.exists(current_item), f'{current_item} does not exist'
            check_files_recursively(children, [*previous_dirs, item])
    elif type(file_structure) is list:
        for item in file_structure:
            current_item = os.path.join(*previous_dirs, item)
            assert os.path.exists(current_item), f'{current_item} does not exist'

@pytest.mark.parametrize('root', [
    {
        'application': {
            'controllers': [
                'api.py',
                'auth.py',
                'routes.py'
            ],
            'forms': [
                '__init__.py',
                'login_form.py',
                'sign_up_form.py'
            ],
            'images': [
                '.gitignore'
            ],
            'models': [
                'ball.py',
                'history.py',
                'user.py'
            ],
            'static': {
                'css': [
                    'dark-forms.css',
                    'styles.css'
                ],
                'img': [
                    'favicon.png',
                    'menu.png',
                    'wallpaper.jpg'
                ],
                'js': [
                    'cam_input.js',
                    'drawing_input.js',
                    'file_input.js',
                    'plot.js'
                ]
            },
            'templates/includes': [
                'cam_input.html',
                'drawing_input.html',
                'file_input.html',
                'footer.html',
                'interface.html',
                'macros.html',
                'nav.html'
            ],
            'templates': [
                'about.html',
                'dashboard.html',
                'home.html',
                'layout.html',
                'login.html',
                'sign-up.html'
            ],
            'utils': [
                'io_utils.py',
                'prediction_utils.py'
            ]
        }
    },
    {
        'application': [
            '__init__.py',
            '.gitignore',
            'config_development.cfg',
            'config_production.cfg',
            'config_staging.cfg',
            'config_testing.cfg'
        ]
    },
    {
        'tests': [
            'conftest.py',
            'test_apis.py',
            'test_models.py',
            'test_unexpected_failures.py'
        ]
    },
    {
        '.': [
            '.dockerignore',
            '.gitignore',
            'app.py',
            'Dockerfile',
            'entrypoint.sh',
            'gunicorn_config.py',
            'README.md',
            'requirements.txt'
        ]
    }
])
def test_files(root):
    check_files_recursively(root)
