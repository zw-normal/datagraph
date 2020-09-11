import os
import subprocess

if __name__ == '__main__':
    print(os.getcwd())
    print(subprocess.check_output(['git', 'diff', '--name-status', 'origin/master', 'HEAD']).decode().split())
    print(subprocess.check_output(['git', 'diff', '--name-only', 'origin/master', 'HEAD']).decode().split())
