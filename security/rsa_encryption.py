import rsa
import os
from sockets.log import Log


# Generate RSA keys to encrypt the communication between client and server sockets
def generate_keys(scope):
    # Check if the public and private keys already exist
    public_key_exist = os.path.isfile(f"./security/rsa_keys/{scope}/public.key")
    private_key_exist = os.path.isfile(f"./security/rsa_keys/{scope}/private.key")

    # If one of the keys does not exist, it generates them
    if not public_key_exist or not private_key_exist:
        Log('OKCYAN', 'SECURITY', 'Generating RSA keys...')
        public_key, private_key = rsa.newkeys(2048)

        # Try to save the generated keys in a .key files
        try:
            with open(f"./security/rsa_keys/{scope}/public.key", "wb") as f:
                f.write(public_key.save_pkcs1("PEM"))

            with open(f"./security/rsa_keys/{scope}/private.key", "wb") as f:
                f.write(private_key.save_pkcs1("PEM"))
            
            Log('OKCYAN', 'SECURITY', 'RSA keys generated successfully!')

        except:
            Log('FAIL', 'SECURITY', 'Unable to save RSA keys')
            return False
        
    return True


# Load de RSA public and private keys from the .key files
def load_rsa_keys(scope):
    Log('OKCYAN', 'SECURITY', 'Loading RSA keys...')

    try:
        with open(f"./security/rsa_keys/{scope}/public.key", "r") as f:
            public_key = f.read()

        with open(f"./security/rsa_keys/{scope}/private.key", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        
        Log('OKCYAN', 'SECURITY', 'RSA keys successfully loaded!')
        return [public_key, private_key]

    except:
        Log('FAIL', 'SECURITY', 'Unable to load RSA keys')
