import socket
import threading
import json
import shutil
import os

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
                connection = {"type": "connect_ack", "payload" : {"message" : name + " connected to the room: " + room}}
                json_connection = json.dumps(connection)
                for client in clients:
                    client.send(json_connection.encode('utf-8'))

            elif info_client["type"] == "message":
                for client in clients:
                    client.send(message.encode('utf-8'))
            elif info_client["type"] == "upload":
                src = payload["src"]
                dst = payload["dst"]
                room = payload["room"]
                uploader = payload["sender"]
                name_file = payload["name_file"]
                with open(dst, 'wb') as temp_file:
                    shutil.copy(src,dst)

                upload_complete = {"type": "message", "payload" : {"sender" : name, "room" : room, "text": "uploaded file " + name_file}}
                upload_json = json.dumps(upload_complete)
                for client in clients:
                    client.send(upload_json.encode('utf-8'))
            elif info_client["type"] == "download":
                src = payload["src"]
                dst = payload["dst"]
                room = payload["room"]
                receiver = payload["receiver"]
                name_file = payload["name_file"]
                with open(dst, 'wb') as temp_file:
                    shutil.copy(src,dst)

                download_complete = {"type": "message", "payload" : {"sender" : name, "room" : room, "text": name + " downloaded file " + name_file}}
                upload_json = json.dumps(download_complete)
                for client in clients:
                    client.send(upload_json.encode('utf-8'))
        
    clients.remove(client_socket)
    client_socket.close()
clients = []

while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target = handle_client, args =(client_socket,client_address))
    client_thread.start()
