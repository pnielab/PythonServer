#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


"""
This is just a loop that waits forever for incoming connections and as soon as it gets one,
it logs the connection (prints some of the connection details) and sends the connected client a welcome message.
Then it stores the client’s address in the addresses dictionary and later starts the handling thread for that client
"""
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()



"""
Naturally, after we send the new client the welcoming message, 
it will reply with the name s/he wants to use for further communication. 
In the handle_client() function, the first task we do is we save this name, and then send another message to the client, 
regarding further instructions. After this comes the main loop for communication: 
here we recieve further messages from the client and if a message doesn’t contain instructions to quit, 
we simply broadcast the messsage to other connected clients (we’ll be defining the broadcast method in a moment). 
If we do encounter a message with exit instructions (i.e., the client sends a {quit}), 
we echo back the same message to the client (it triggers close action on the client side) and then we close the connection socket for it. 
We then do some cleanup by deleting the entry for the client, 
and finally give a shoutout to other connected people that this particular person has left the conversation.
"""
def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

"""
it simply sends the msg to all the connected clients, and prepends an optional prefix if necessary. 
We do pass a prefix to broadcast() in our handle_client() function, and we do it so that people can see exactly who is the sender of a particular message.

"""
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

"""
We join() ACCEPT_THREAD so that the main script waits for it to complete and doesn’t jump to the next line, which closes the server.
"""
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()