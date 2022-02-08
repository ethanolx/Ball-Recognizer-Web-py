import os
import glob
import shutil

try:
    os.remove('application/database.db')
except:
    pass
finally:
    for f in glob.glob('application/images/*.png'):
        os.remove(f)

    for f in glob.glob('**/__pycache__', recursive=True):
        shutil.rmtree(f, ignore_errors=True)

    shutil.rmtree('.pytest_cache', ignore_errors=True)