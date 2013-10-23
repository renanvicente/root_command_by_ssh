#!/usr/bin/python
# -*- encoding: utf8 -*-
# Author: Renan Vicente Gomes da Silva <renanvice@gmail.com>

from sys import argv, exit
from pxssh import pxssh , ExceptionPxssh
from getpass import getpass
from pexpect import ExceptionPexpect
import re


green = '\033[1;32m'
yellow = '\033[1;33m'
blue = '\033[1;34m'
red = '\033[1;31m'
end_color = '\033[m'




def getInfo(root=False):
    try:
        info = {}
        info['username'] = raw_input('username: ')
        info['password'] = getpass('password: ')
        if root:
            info['root'] = getpass('root password: ')
        info['command'] = raw_input('Insert command to execute: ')
    except KeyboardInterrupt:
        exit(1)
    return info


def doSSH(hostname, username, password, command, root=False, port_number=13000):
    try:
        s = pxssh()
        s.login(hostname, username, password, port=port_number, login_timeout=5)
        ret=0
        c=1
        while(ret != c and c <= 2):
            if root:
                try:
                    s.sendline('''su - -c "''' + command + '''"''')
                    s.expect("([Ss]enha:)|([Pp]assword:)")
                    s.sendline(root)
                    s.prompt()
                    if re.search(r'(?i)(falha)|(failed)|(incorrect)', s.before.split('\n')[1]):
                        c=c+1
                        if c == 2:
                            print(red + 'Machine: %s ROOT incorrect password' % hostname + end_color)
                    else:
                        print(green + "Machine: %s Result: %s" % (hostname, s.before.split('\n')[1]) + end_color)
                        ret=c
                except:
                    c=c+1
            else:
                try:
                    s.sendline(command)
                    s.prompt()
                    print(green + "User: %s Machine: %s Result: %s" % (username, hostname, s.before.split('\n')[1]) + end_color)
                    ret=c
                except:
                    c=c+1
        if c == 2:
            print(red + "\n\n %s ROOT password failed." % hostname + end_color)
            exit(1)
            s.logout()
    except ExceptionPxssh as e:
        print(red + "\n\n %s Fail first Login." % hostname + end_color)
        print(yellow + str(e) + "\n\n" + end_color)
    except  ExceptionPexpect as e:
        print(red + "\n\n %s Problem with ssh port or incorret password." % hostname + end_color)
        print(str(e) + "\n\n")
    except KeyboardInterrupt:
        exit(1)
  
def main():
    args = argv[1:]

    if not args:
        print(blue + 'Usage: [--tofile] host [host ...].\nTry --help' + end_color)
        exit(1)
    if len(args) == 0:
        print(red + 'error: must specify one host' + end_color)
        exit(1)

    tofile = ''    
    if '--file' in args:
        start = args.index('--file')
        end = start + 1
        try:
            tofile = args[end]
            del args[start:end]
        except IndexError:
            print(blue + 'Usage: [--tofile] host [host ...].\nTry --help' + end_color)
            exit(1)

    port = ''
    if '--port' in args:
        start = args.index('--port')
        end = start + 1
        try:
            port = args[end]
            del args[end]
        except IndexError:
            print(blue + 'Usage: [--tofile] host [host ...].\nTry --help' + end_color)
            exit(1)

    root = ''
    if '--root' in args:
        end = args.index('--root')
        root = True
        del args[end]


    tohelp = ''
    if '--help' in args:
        tohelp = True

    hosts = []

    if tohelp:
        print(blue + """
        MultiHost script command
        Author: Renan Vicente Gomes da Silva <renanvice@gmail.com>

        Usage: [--root][--file][--port] host [host ...]

        --root:     Run on administrator mode, execute commands as root

        --file FILE:     Especify file with list about hosts

        --port PORT:     Especify port different statement [ DEFAULT=13000]

        --help:     Short description about arguments

        """ + end_color)
        exit()



    if tofile:
        try:
            filename = open(tofile, 'r')
            for line in filename:
                hosts.append(line)
        except IOError:
            print('%s cannot be read' % tofile)
            exit(1)
    else:
        for host in args:
            hosts.append(host)

    if root:
        info = getInfo(True)
    else:
        info = getInfo()
    for host in hosts:
        if root:
            if port:
                doSSH(host, info['username'], info['password'], info['command'], info['root'] , port)
            else:
                doSSH(host, info['username'], info['password'], info['command'], info['root'])
        elif port:
            doSSH(host , info['username'] , info['password'], info['command'], False, port)
        else:
            doSSH(host , info['username'] , info['password'], info['command'])


if __name__ == '__main__':
    main()


