import socket
import logging
import json
import os


class DBClient:
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    server = ''
    port = ''
    client = None

    def __init__(self, server: str = os.getenv('FNA_DBSERVER_ADDR', '127.0.0.1'), port: int = int(os.getenv('FNA_DBSERVER_PORT', '20002'))):
        self.server = server
        self.port = port


    def connect(self):
        '''[INTERNAL] Function to connect to the server.'''
        self.log.debug('Connecting to server...')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server, self.port))
        self.log.debug('Connected to server')

    def close(self):
        '''[INTERNAL] Function to close the connection.'''
        self.client.shutdown(socket.SHUT_RDWR)
        self.log.debug('Connection closed')

    def send_data(self, data: dict) -> dict:
        '''[INTERNAL] Function to send data to the server.'''
        return_val = None
        self.log.info(f"Sending data: {data}")
        dd = json.dumps(data)
        self.log.debug(f"Encoded data: {dd}")
        self.client.sendall(dd.encode())

        try:
            message = self.client.recv(1024)
            if not message:
                self.log.warning("Disconnected from the server.")
                return_val = {'error': 'Disconnected from the server.'}
            self.log.debug(f"Received: {message.decode()}")
            return_val = json.loads(message.decode())
        except Exception as e:
            self.log.error(f"Error receiving message: {e}")
            return_val = {'error': f"Error receiving message: {e}"}

        return return_val

    def set_value(self, key: str, value):
        '''Function to set a value in the database.'''
        answer = self.send_data({'act': 'set', 'key': key, 'val': value})
        if 'error' in answer:
            self.log.error(answer['error'])
            raise Exception(answer['error'])
        elif 'key' not in answer or 'val' not in answer:
            self.log.error(f'response is not valid: {answer}')
            raise Exception(f'response is not valid: {answer}')
        else:
            return answer['val']

    def get_value(self, key: str):
        '''Function to get a value from the database.'''
        answer = self.send_data({'act': 'get', 'key': key})
        if 'error' in answer:
            self.log.error(answer['error'])
            raise Exception(answer['error'])
        elif 'key' not in answer or 'val' not in answer:
            self.log.error(f'response is not valid: {answer}')
            raise Exception(f'response is not valid: {answer}')
        else:
            return answer['val']
