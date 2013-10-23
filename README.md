h1. root_command_by_ssh

This script is to execute remote command,
by simple user or root, you can take a list of ips and use script to execute commands

h2. Using

<pre>
<code>
    1. Clone
    git clone git@github.com:renanvice/root_command_by_ssh.git
    cd root_command_by_ssh

    2. Exemple to run
    chmod u+x multihost_shell.py
    2.1 Execute command as root
    ./multihost_shell.py --root 192.168.1.104
    2.2 Using file text with list ips
    ./multihost_shell.py --root --file list_ips.txt
    2.3 You can use --help to see more options
    ./multihost_shell.py --help

    3. Execution
    You will be asked to inform the simple user , simple user password and root password.
    The script will sign in with simple user and than use command su to execute command as root

</code>
</pre>

h2. Author

Renan Vicente Gomes da Silva <renanvice [at] gmail [dot] com>
http://linuxextreme.org

