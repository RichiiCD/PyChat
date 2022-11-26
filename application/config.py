import socket
import json
import os


# Read the content from the configuration file
def read_configuration_file():
    config_file = open('settings.json')
    json_data = json.load(config_file)
    return json_data


# Configure the remote/local server
def configure_server(type):
    server_configuration = {}

    if (type == 'server'):
        scope = 'Local'
    else:
        scope = 'Remote'

    server = input(f'> {scope} sever address [Local]: ')

    if (server):
        server_configuration['address'] = server
    else:
        server_configuration['address'] = socket.gethostbyname(socket.gethostname())

    try:
        port  = int(input(f'> {scope} server port [5050]: '))
    except ValueError:
        port = 5050
    
    server_configuration['port'] = port

    return server_configuration


# Configure the application and server settings
def configure_application():
    config = {}

    os.system('cls' if os.name == 'nt' else 'clear')

    print('- Client chat interface configuration [interface]')
    print('- Local server configuration [server]')
    print('- Remote server configuration [client]')
    config_type = input('> Config type: ')
    type = config_type

    os.system('cls' if os.name == 'nt' else 'clear')

    if (config_type == 'interface'):
        config['bg_color'] = input('> Background color: ')
        config['bg_button'] = input('> Background button : ')
        config['text_color'] = input('> Text color: ')
        config['font'] = input('> Font: ')

    elif (config_type == 'server' or config_type == 'client'):
        config = configure_server(type)

    else:
        print('! Invalid option')
        return False

    # Read the current configuration
    json_data = read_configuration_file()

    json_data[type] = config
    
    json_data = json.dumps(json_data)

    # Save the new configuration
    with open(".\settings.json", "w") as outfile:
        outfile.write(json_data)
    
    print('Config successfully updated!')


