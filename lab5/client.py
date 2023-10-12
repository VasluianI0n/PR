import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
x = 0
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
client_socket.connect((HOST, PORT))
print(f"Coonected to {HOST}:{PORT}")

def receive_messages():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        info_client = json.loads(message)
        payloadjson = json.dumps(info_client["payload"])
        payload = json.loads(payloadjson)
        if info_client["type"] == "connect_ack":
                print(payload["message"])
        elif info_client["type"] == "message":
                print(payload["sender"]+": "+payload["text"])



name = input("Type your username: ")
room = input("Type the room you want to get into: ")

info_client= {"type": "connect", "payload" : {"name" : name, "room" : room}}

json_info = json.dumps(info_client)

client_socket.send(json_info.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()


while True:
    
    message = input("")

    if message.lower() == 'exit':
        break
    
    formatted_message = {"type": "message", "payload" : {"sender" : name, "room" : room, "text": message}}
    json_message = json.dumps(formatted_message)
    client_socket.send(json_message.encode('utf-8'))

    

client_socket.close()