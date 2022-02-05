import os
import glob
import shutil

os.remove('application/database.db')

for f in glob.glob('**/__pycache__', recursive=True):
    shutil.rmtree(f)
