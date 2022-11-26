import socket
import rsa
import threading
import pickle
import os
from .custom_socket import CustomSocket
from .log import Log
from application import read_configuration_file


class ServerSocket(CustomSocket):
    ''' Chat application server socket class'''

    def __init__(self, header):
        os.system('cls' if os.name == 'nt' else 'clear')

        # Read the JSON config file and load the server configuration
        json_config = read_configuration_file()['server']

        # Initialize the parent socket by passing the required arguments
        super().__init__('server', header, (json_config['address'], json_config['port']), 'utf-8')

        # Client and connections list containing the active clients sockets connections and their information 
        self.client_list = {}
        self.connection_list = []
        self.status = 'open'

    # Called before the server starts. Configures the initial options
    def setup(self):
        Log('OKGREEN', 'STARTING', 'Server is starting')

        # Allow connections from clients with the same address
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Try to bind on configured server address
        try:
            self.conn.bind(self.server)
            return True

        except OSError:
            Log('FAIL', 'SERVER ERROR', f'Unable to bind on server {self.server[0]}:{self.server[1]}')
            return False
    
    # Send the client's message to all the clients in the same room
    def send_broadcast_message(self, msg, sender_conn):
        sender_user = self.client_list[sender_conn]
        decoded_msg = pickle.loads(msg)['message']

        for client, user in self.client_list.items():

            if sender_user['room'] == user['room']:
                msg = pickle.dumps({'username': sender_user['username'], 'message': decoded_msg})
                encrypted_msg = self.encrypt_message(msg, user['public_key'])
                msg_header  = f"{len(encrypted_msg):<{self.header}}".encode('utf-8')

                client.send(msg_header + encrypted_msg)

    # Handle a received client's message
    def receive_message(self, conn):
        try:
            message_header = conn.recv(self.header)
            
            if not len(message_header):
                return False
            
            message_length = int(message_header.decode('utf-8'))
            return {'header': message_header.decode('utf-8'), 'data': conn.recv(message_length)}

        except:
            return False

    # Handle client socket connection
    def client_handler(self, conn, addr):
        ''' Every client connections runs into different thread '''

        Log('OKBLUE', 'NEW CONNECTION', f'{addr} connected')
        connected = True

        while connected:
            encrypted_message = self.receive_message(conn)

            # If no message received from client, the connection is closed and the client is removed from the list
            if encrypted_message is False:
                Log('OKBLUE', 'CONNECTION CLOSED', f'{addr[0]} closed the connection')
                connected = False
                self.connection_list.remove(conn)
                del self.client_list[conn]
                conn.close()
                continue
            
            message = self.decrypt_message(encrypted_message['data'])

            self.send_broadcast_message(message, conn)

    # Called after the server setup. Event loop to accept and handle new clients connections.
    def run(self):
        # Check if the public and private RSA keys are correctly loaded
        if not self.private_key or not self.public_key:
            Log('FAIL', 'RUNNING ERROR', 'Unable to run server: RSA keys not loaded')
            return False

        # Server socket starts listening for new connections from client sockets 
        self.conn.listen()
        Log('OKGREEN', 'LISTENING', f'Server is listening on {self.server}')

        while True:
            # Wait to receive a new connection
            conn, addr = self.conn.accept()

            # Send its public key to client
            self.send_public_key(conn)

            # Receive the public key from the client
            client_public_key = self.receive_message(conn)

            if client_public_key is False:
                continue
            
            # Receive the client configuration data
            encrypted_client_user = self.receive_message(conn)

            if encrypted_client_user is False:
                continue
            
            # Decrypts the configuration data with its private key
            client_data = self.decrypt_message(encrypted_client_user['data'])
            client_data = pickle.loads(client_data)
    
            client_data['public_key'] = rsa.PublicKey.load_pkcs1(client_public_key['data'])
            
            # Save the user configuration and information data
            self.connection_list.append(conn)
            self.client_list[conn] = client_data

            # Create a thread to handle client socket connection
            thread = threading.Thread(target=self.client_handler, args=(conn, addr))
            thread.start()
    