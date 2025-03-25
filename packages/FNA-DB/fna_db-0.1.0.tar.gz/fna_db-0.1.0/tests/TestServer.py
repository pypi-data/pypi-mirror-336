import queue
import socket
import threading
import json
import os


class TestServer:
    # Set up the server address and port
    server_address = (os.getenv('FNA_DBSERVER_BIND_ADDR', '127.0.0.1'), int(os.getenv('FNA_DBSERVER_PORT', '20002')))

    # Create a TCP/IP socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(server_address)
    server_sock.listen(5)  # Set a queue for a maximum of 5 connections

    #print(f"Server is listening on {server_address}")

    # List to keep track of connected clients
    clients = []

    # The In Memory Database
    db = {'version': 0}

    def handle_client(self, connection, client_address):
        """Function to handle client connection."""
        #print(f"Connection from {client_address}")
        self.clients.append(connection)  # Add new client to the list
        try:
            while True:
                # Receive data from client
                data = connection.recv(1024)
                if not data:
                    #print(f"No data from {client_address}. Closing connection.")
                    break  # No more data from the client

                #print(f"Received from {client_address}: {data.decode()}")
                # Forward the received message to all clients
                answer = self.handle_request(data.decode())
                self.answer_message(answer.encode(), connection)

        except Exception as e:
            pass
            # print(f"Error with {client_address}: {e}")
        finally:
            self.clients.remove(connection)  # Remove client from list on disconnect
            connection.close()
            #print(f"Connection with {client_address} closed.")

    def handle_request(self, request):
        """Function to handle incoming requests."""
        if self.is_jsonable(request):
            req_dict = json.loads(request)
            if 'act' in req_dict and 'key' in req_dict:
                if req_dict['act'] == 'get':
                    # Get Value from Key as Dict
                    return json.dumps(self.get_db_key(req_dict['key']))
                elif req_dict['act'] == 'set':
                    if 'val' in req_dict:
                        # Set Value from Key
                        self.set_db_key(req_dict['key'], req_dict['val'])
                    else:
                        self.set_db_key(req_dict['key'], '')
                    # GetValue from Key as Dict
                    return json.dumps(self.get_db_key(req_dict['key']))
            else:
                return json.dumps({'error': 'Invalid parameters, act and key are required'})
        else:
            return json.dumps({'error': 'Invalid format'})

    def set_db_key(self, key, value):
        self.db[key] = value

    def get_db_key(self, key):
        if key in self.db:
            return {'key': key, 'val': self.db[key]}
        else:
            return {'key': key, 'val': ''}

    def is_jsonable(self, x):
        try:
            json.loads(x)
            return True
        except:
            return False

    def answer_message(self, message, sender_connection):
        """Function to forward the message to all connected clients except the sender."""
        for client in self.clients:
            if client == sender_connection:  # Don't send the message back to the sender
                try:
                    client.sendall(message)  # Forward message to the other clients
                except Exception as e:
                    pass
                    # #print(f"Failed to send message to {client}: {e}")

    def run_server(self):
        """Function to start the server."""
        try:
            connection, client_address = self.server_sock.accept()
            # Start a new thread for each client connection
            self.handle_client(connection, client_address)
        except Exception as e:
            pass
