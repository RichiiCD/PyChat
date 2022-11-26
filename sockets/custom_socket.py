import socket
import rsa
from security.rsa_encryption import generate_keys, load_rsa_keys


class CustomSocket:
    ''' Custom socket parent class for the server/client sockets inherit '''

    def __init__(self, type, header, server, format):
        self.header = header
        self.server = server
        self.format = format
        self.type = type
        self.private_key = None
        self.public_key = None
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Check if the RSA public/private keys were successfully generated
        successfully_keys_generated = self.generate_rsa_keys()

        if (successfully_keys_generated):
            # If the RSA keys are generated, load and save them from the .key files 
            loaded_keys = load_rsa_keys(self.type)
            if (loaded_keys):
                self.public_key, self.private_key = loaded_keys

    # Call the generate_keys function before the sockets connection 
    def generate_rsa_keys(self):
        return generate_keys(self.type)
    
    # Send the RSA public key between sockets
    def send_public_key(self, conn):
        key_header = f"{len(self.public_key):<{self.header}}".encode('utf-8')
        conn.send(key_header + self.public_key.encode('utf-8'))
    
    # Encrypt a message with the public key of destination socket
    def encrypt_message(self, msg, public_key):
        encrypted_msg = rsa.encrypt(msg, public_key)
        return encrypted_msg

    # Decrypt a encrypted message with the current socket private key
    def decrypt_message(self, encrypted_msg):
        decrypted_msg = rsa.decrypt(encrypted_msg, self.private_key)
        return decrypted_msg

