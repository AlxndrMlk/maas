import os
import git
import time

git_folder = os.getcwd()

print(f'\nLocated project folder: {git_folder}')
time.sleep(3)

print(f'Pulling...')

g = git.cmd.Git(git_folder)
g.pull()

print(f'Done.')
time.sleep(3)