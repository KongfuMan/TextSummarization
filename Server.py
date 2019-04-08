import socket

# import thread module
from _thread import *
import threading

# print_lock = threading.Lock()


# thread fuction
def threaded(clientSocket):
    while True:
        # data received from client
        data = clientSocket.recv(1024)
        print("Thread "+threading.currentThread().getName() + "receives msg ")
        if not data:
            print('Bye')

            # lock released on exit
            # print_lock.release()
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        clientSocket.send(data)

        # connection closed
    clientSocket.close()


def Main():
    host = "127.0.0.1"

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 60001
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    serverSocket.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        clientSocket, addr = serverSocket.accept()

        # lock acquired by client
        # print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (clientSocket,))
    serverSocket.close()


if __name__ == '__main__':
    Main()