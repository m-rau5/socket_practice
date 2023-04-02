import socket

HOST = input("Enter Server IP Address:")
PORT = int(input("Enter Server PORT:"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    try:
        clientSocket.connect((HOST, PORT))
    except:
        print("Cannot connect to the server")
        exit()

    while True:
        try:
            # wait for data from server
            data = clientSocket.recv(1024)

            print("Message received: " + data.decode())

            message = bytes(input("\nEnter message:").encode())
            while not message:
                message = bytes(
                    input("\nMessage cannot be empty.\nEnter message:").encode())

            # If we send "!close", it will kill the calling client
            if message == b"!disconnect":
                print("Killing client...")
                clientSocket.sendall(message)
                exit()
            else:  # if not just send the message
                clientSocket.sendall(message)
        except:  # if exception just close the connection
            clientSocket.sendall(b"!close")
            exit()
