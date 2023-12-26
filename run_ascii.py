from subprocess import Popen, CREATE_NEW_CONSOLE

Popen(['python3', 'client_bigascii.py'], creationflags=CREATE_NEW_CONSOLE)
Popen(['python3', 'server_bigascii.py'], creationflags=CREATE_NEW_CONSOLE)