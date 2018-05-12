#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
"""
https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
"""


"""
This is more fun beause we’ll be writing a GUI! We use Tkinter, Python’s “batteries included” GUI building tool for our purpose. Let’s do some imports 
"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

"""
Now we’ll write functions for handling sending and receiving of messages. We start with receive:
Why an infinite loop again? Because we’ll be receiving messages quite non-deterministically, 
and independent of how and when we send the messages. We don’t want this to be a walkie-talkie chat app which can only either send or receive at a time; 
we want to receive messages when we can, and send them when we want. The functionality within the loop is pretty straightforward; 
the recv() is the blocking part. It stops execution until it receives a message, and when it does, 
we move ahead and append the message to msg_list. We will soon define msg_list, 
which is basically a Tkinter feature for displaying the list of messages on the screen.
"""
def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


"""
We’re using event as an argument because it is implicitly passed by Tkinter when the send button on the GUI is pressed. 
my_msg is the input field on the GUI, and therefore we extract the message to be sent usin g msg = my_msg.get(). After that, 
we clear the input field and then send the message to the server, which, as we’ve seen before, broadcasts this message to all the clients (if it’s not an exit message). 
If it is an exit message, we close the socket and then the GUI app (via top.close())

We define one more function, which will be called when we choose to close the GUI window. 
It is a sort of cleanup-before-close function and shall close the socket connection before the GUI closes
This sets the input field to {quit} and then calls send(), which then works as expected. Now we start building the GUI, 
in the main namespace (i.e., outside any function). We start by defining the top-level widget and set its title:
"""

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() # Starts GUI execution.


