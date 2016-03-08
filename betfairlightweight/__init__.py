import subprocess

__version__ = '0.0.1'
__git_version__ = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode("utf-8").strip()
