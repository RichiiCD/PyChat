import tkinter as tk
from sockets.client import ClientSocket
from application import LoginInterface, ChatInterface
from .config import read_configuration_file


class ChatApplication:
    ''' Client chat application '''
    
    def __init__(self):
        self.chat_root = tk.Tk()
        
        # Load and display the Login windows
        self.home = LoginInterface(self.chat_root, self.start_chat)
        self.home.display()

    # Start the chat application after login windows 
    def start_chat(self, event=None):
        client_data = self.home.get_input_value()
        self.home.close_tab()

        # Load the interface configuration from JSON file
        json_config = read_configuration_file()['client']

        # Create the client socket
        self.socket = ClientSocket(client_data, 64, (json_config['address'], json_config['port']),  'utf-8', on_message=self.recive_message_handler)

        # After client socket is successfully setup, display the chat interface
        if (self.socket.setup()):
            # Start the connection between client and server sockets
            self.socket.start()

            self.home_root = tk.Tk()

            self.chat = ChatInterface(self.home_root, client_data['room'], on_close=self.close, send_message=self.send_message_handler)
            self.chat.display()

    # Pass the received messages from client socket to chat interface
    def recive_message_handler(self, messaage):
        self.chat.new_message(messaage)

    # Pass the sended message from chat interface to client socket
    def send_message_handler(self, event=None):
        message =  self.chat.get_input_value()
        self.socket.send(message)

    # Close the application
    def close(self):
        self.socket.status = 'closed'
        self.chat.close_tab()