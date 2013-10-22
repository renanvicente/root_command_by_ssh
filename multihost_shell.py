#!/usr/bin/python
# -*- encoding: utf8 -*-
#
from sys import argv, exit
from pxssh import pxssh , ExceptionPxssh
from getpass import getpass
from pexpect import ExceptionPexpect


def getInfo(root=False):
    info = {}
    info['username'] = raw_input('username: ')
    info['password'] = getpass('password: ')
    if root:
        info['root'] = getpass('root password: ')
    return info


def doSSH(hostname, username, password, port=22, root=False):
    try:
        s = pxssh()
        s.login(hostname, username, password, port , login_timeout=5)
        s.sendline('hostname')
        s.prompt()
        txt = s.before.split('\n')
        ret=0
        c=1
        while(ret != c and c < 4):
            if root:
                try:
                    ########## COMANDO A SER EXECUTADO COMO ADMINISTRADOR #########
                    s.sendline('''su - -c "useradd mauricio"''')
                    s.expect("([Ss]enha:)|([Pp]assword)")
                    s.sendline(root)
                    s.prompt()
                    print("Machine: %s Result: %s" % (hostname, s.before.split('\n')[1]))
                    ret=c
                except:
                    c=c+1
            else:
                try:
                    ######### COMANDO A SER EXECUTADO COMO USUARIO COMUM ######
                    s.sendline(''' hostname ''')
                    s.prompt()
                    print("User: %s Machine: %s Result: %s" % (username, hostname, s.before.split('\n')[1]))
                    ret=c
                except:
                    c=c+1
        if c == 4:
            print("\n\n %s fail first login." % hostname)
            exit(1)
            s.logout()
    except ExceptionPxssh, e:
        print("\n\n %s Fail first Login." % hostname)
        print(str(e) + "\n\n")
    except  ExceptionPexpect, e:
        print("\n\n %s Problema de acesso a porta do ssh." % hostname)
        #print(str(e) + "\n\n")
  
def main():
    args = argv[1:]

    if not args:
        print('Usage: [--tofile] host [host ...].\nTry --help')
        exit(1)
    if len(args) == 0:
        print('error: must specify one host')
        exit(1)

    tofile = ''    
    if '--file' in args:
        start = args.index('--file')
        end = start + 1
        tofile = args[end]
        del args[start:end]

    port = ''
    if '--port' in args:
        end = args.index('--port')
        port = True
        del args[end]

    root = ''
    if '--root' in args:
        end = args.index('--root')
        root = True
        del args[end]

    hosts = []

    if tofile:
        filename = open(tofile, 'r')
        for line in filename:
            hosts.append(line)
    else:
        for host in args:
            hosts.append(host)


    if root:
        info = getInfo(True)
    else:
        info = getInfo()
    for host in hosts:
        if port or root:
            if info['root']:
                doSSH(host, info['username'], info['password'], port, info['root'])
            else:
                doSSH(host, info['username'], info['password'], port)
        else:
            doSSH(host , info['username'] , info['password'])

if __name__ == '__main__':
    main()


