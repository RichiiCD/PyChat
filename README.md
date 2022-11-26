# PyChat: A Python-Based Secure Chat Room
[![PyPI](https://img.shields.io/pypi/v/rsa.svg)](https://pypi.org/project/rsa/)

Advanced Python-based secure chat room application using socket library. All the project is entirely developed using socket library for client/server connection and rsa library for communication encryption. Run the server with a specific IP Address and Port, then open the client interface and logging with the username and the chat room ID. 


## Who does it works?

When the client sends a message, it is encrypted with the remote server public RSA key. The encrypted message is received by the server, which will decrypt it with its private RSA key. Then, the server sends the message to all the members of the room, first encrypting it with their corresponding public RSA keys. These clients receive the encrypted message and decrypt it with their private RSA key.

## How to install?

- Download the source code from this repo.
- Install Python 3.9
- Install the required packages:

```Python
python -m pip install requirements.txt
```

## How to start?

To configure the client or server, run the following command and follow the wizard to configure the local server:

```Python
python main.py settings
```

Run the server:

```Python
python main.py runserver
```

Run the client:

```Python
python main.py chat
```
