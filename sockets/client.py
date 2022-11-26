import sys
import os
import errno
import threading
import rsa
import pickle
import socket
from .custom_socket import CustomSocket
from .log import Log


class ClientSocket(CustomSocket):
    ''' Chat application client socket class'''

    def __init__(self, client_data, header, server, format, on_message):
        os.system('cls' if os.name == 'nt' else 'clear')

        # Initialize the parent socket by passing the required arguments
        super().__init__('client', header, server, format)
        self.status = 'close'
        self.username = client_data['username']
        self.room = client_data['room']
        self.on_message = on_message
        self.remote_public_key = None
    
    # Called before the client socket connection starts. Configures the initial options
    def setup(self):
        Log('OKCYAN', 'CONNECTING', 'Connecting to remote server...')
        remote_server = f"{self.server[0]}:{self.server[1]}"

        # Try to connect to remote server
        try:
            self.conn.connect(self.server)
            self.status = 'open'
            Log('OKGREEN', 'CONNECTING', f'Connection established with remote server ({remote_server})')
            return True

        except ConnectionRefusedError:
            Log('FAIL', 'CONNECTION ERROR', f'Connection refused by remote server')
            
        except TimeoutError:
            Log('FAIL', 'CONNECTION ERROR', f'Unable to connect to remote server ({remote_server})')
        
        except socket.gaierror:
            Log('FAIL', 'CONNECTION ERROR', f'Error on remote server ({remote_server}) configuration')
        
        return False

    # Called after the client setup. Configures communication with the remote server
    def start(self):
        if (self.status == 'open'):
            self.conn.setblocking(False)

            # Receive the public RSA key from the remote server
            received_key = self.receive_public_key()
            if not received_key:
                sys.exit()
            
            self.remote_public_key = received_key

            # Send its public key to remote server
            self.send_public_key(self.conn)
            
            # Send the client configuration 
            self.client_config()

            # Create a thread for handle receiving messages
            t = threading.Thread(target=self.receive)
            t.start()

    # Configures and send the client options (username, room) to remote server 
    def client_config(self):
        client_data = {'username': self.username, 'room': self.room}
        msg = pickle.dumps(client_data)

        encrypted_msg = self.encrypt_message(msg, self.remote_public_key)

        msg_header  = f"{len(encrypted_msg):<{self.header}}".encode('utf-8')
        self.conn.send(msg_header + encrypted_msg)

    # Function to handle receiving messages from the remote server
    def receive(self):
        while self.status == 'open':
            try:
                data_header = self.conn.recv(self.header)

                # If the received header message has no length, the connection is closed
                if not len(data_header):
                    Log('FAIL', 'CLOSED CONNECTION', 'Connection closed by the remote server')
                    sys.exit()

                # Receive the rest of the message
                data_length = int(data_header.decode('utf-8'))
                encrypted_data = self.conn.recv(data_length)

                # Decrypt the received message
                data = self.decrypt_message(encrypted_data)
                data = pickle.loads(data)

                self.on_message({'username': data['username'], 'message': data['message']})        

            # If no input from socket connection, continue and try again 
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    self.conn.close()
                    Log('FAIL', '[READING ERROR]', 'Connection closed by remote server')
                    sys.exit()
                continue

            except Exception as e:
                self.conn.close() 
                Log('FAIL', '[FATAL ERROR]', str(e))
                sys.exit() 

    # Recive the public RSA key from the remote server
    def receive_public_key(self):
        Log('OKCYAN', 'SECURITY', 'Loading remote server RSA public key...')

        # Try to recive the key
        try:
            key_header = self.conn.recv(self.header)
            key_length = int(key_header.decode('utf-8'))
            msg = self.conn.recv(key_length)

            Log('OKCYAN', 'SECURITY', 'Remote server RSA public key loaded successfully!')

            return rsa.PublicKey.load_pkcs1(msg)
        
        except:
            Log('FAIL', 'SECURITY', 'Remote server RSA public key load failed')
    
    # Send a encrypted message to remote server
    def send(self, message):
        if message:
            msg = pickle.dumps({"message": message})

            encrypted_msg = self.encrypt_message(msg, self.remote_public_key)

            msg_header  = f"{len(encrypted_msg):<{self.header}}".encode('utf-8')
            self.conn.send(msg_header + encrypted_msg)
    
