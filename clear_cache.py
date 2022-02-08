import os
import glob
import shutil

shutil.rmtree('application/database.db', ignore_errors=True)

for f in glob.glob('application/images/*.png'):
    os.remove(f)

for f in glob.glob('**/__pycache__', recursive=True):
    shutil.rmtree(f, ignore_errors=True)
