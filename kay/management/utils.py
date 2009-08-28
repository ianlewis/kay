
import sys

def print_status(msg='',nl=True):
  if nl:
    print(msg)
  else:
    print(msg),
  sys.stdout.flush()
