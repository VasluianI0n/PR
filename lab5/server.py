import socket
import threading
import json
# Server configuration
HOST = '127.0.0.1' # Loopback address for localhost
PORT = 12345 # Port to listen on
# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        else:
            info_client = json.loads(message)
            payloadjson = json.dumps(info_client["payload"])
            payload = json.loads(payloadjson)
            if info_client["type"] == "connect":
                name = payload["name"]
                room = payload["room"]
                print(payload)
                for client in clients:
                    connection = {"type": "connect_ack", "payload" : {"message" : name + " connected to the room: " + room}}
                    json_connection = json.dumps(connection)
                    client.send(json_connection.encode('utf-8'))

            elif info_client["type"] == "message":
                for client in clients:
                    client.send(message.encode('utf-8'))

        
    clients.remove(client_socket)
    client_socket.close()
clients = []

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target = handle_client, args =(client_socket,client_address))
    client_thread.start()
