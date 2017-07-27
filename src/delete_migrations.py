import os
import shutil

root_dir = os.getcwd()

for subdir, dirs, files in os.walk(root_dir):
    for directory in dirs:
        if directory == "migrations":
            shutil.rmtree(os.path.join(subdir, directory))
