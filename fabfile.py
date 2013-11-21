from fabric.api import *
from getpass import getpass

cont = 0
info = {}
def get_info(root=False):
  try:
    global info
    if not info:
      info['username'] = raw_input('username: ')
      info['password'] = getpass('password: ')
      if root:
        info['pass_root'] = getpass('root password: ')
      info['command'] = raw_input('Insert command to execute: ')
  except KeyboardInterrupt:
      exit(1)
  return info
  
def run_as_root_with_su():
  info = get_info(True)
  su(info['username'],info['password'], info['command'],info['pass_root'])

def run_as_root_with_sudo():
  info = get_info()
  env.user = info['username']
  env.password = info['password']
  sudo('%s' % info['command'])

def run_as_user_common():
  info = get_info()
  with settings(user='%s' % info['username'], password='%s' % info['password']):
    sudo('%s' % info['command'])

def tofile(filename):
  env.hosts = open('%s' % filename, 'r').readlines()

def su(username,password,command,pass_root):
  with settings(user='%s' % username, password='%s' % password):
    run('whoami')
    with settings(user='root',password='%s' % pass_root, sudo_prefix="su -c", sudo_prompt="Password:"):
      sudo('%s' % command)
