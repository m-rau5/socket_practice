import socket
import _thread

HOST = socket.gethostname()
PORT = int(input("Enter the desired server port:"))
ADDR = (HOST, PORT)

# create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UserNum = 0
connected = True
clientList = dict()


def connectionHandling(connection: socket.socket, address: socket.AddressFamily):
    connection.send(str.encode(
        "User client connected to: " + socket.gethostbyname(HOST) + ":" + str(PORT)))

    global UserNum
    CurrUser = UserNum
    global connected
    while connected:
        # wait to recieve data from the client
        data = connection.recv(1024)
        response = data.decode()

        if response == '!disconnect':
            print("User " + str(CurrUser) + " has disconnected: (" +
                  address[0] + ":\33[95m" + str(address[1]) + ":\33[0m)")
            clientList.pop(CurrUser)
            connection.close()
            return
        elif response.upper() == 'HELLO':
            connection.send("Hello User!".encode())
        else:
            connection.send(response.encode())

        print("User" + str(CurrUser) + ": " + data.decode() +
              " (" + address[0] + ":\33[95m" + str(address[1]) + "\33[0m)")


def startServer():
    print("Server is starting...")

    try:
        server.bind(ADDR)
    except socket.error as err:
        print(err)
        exit()

    # start listening for connections
    print(f"[SERVER IS LISTENING ON: {socket.gethostbyname(HOST)}:{PORT}]")
    server.listen(10)

    while True:
        # waits for a touple of a socket obj and ip/port
        conn, address = server.accept()

        # once new user connects
        global UserNum
        UserNum += 1
        clientList[UserNum] = (conn, address)

        print("User connected: (" +
              address[0] + ":\33[95m" + str(address[1]) + "\33[0m)")
        _thread.start_new_thread(connectionHandling, (conn, address))


startServer()
