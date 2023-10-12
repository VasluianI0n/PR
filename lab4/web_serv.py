import socket
import signal
import sys
import threading
import json
import re

from time import sleep


HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")

def product_names():
    product_names_string = ""
    with open("products.json", "r") as file:
        data = json.load(file)
        for i in range(len(data)):
            element = data[i]
            name = element["name"]
            product_names_string= product_names_string + f"{name} \n"
    return product_names_string

def product_info(index):
    product_full_info = ""
    with open("products.json", "r") as file:
        data = json.load(file)
        if index > len(data):
            return "404 Not Found"
        element = data[index-1]
        product_full_info = element
    return product_full_info

def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n {request_data}")

    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]
    page_number = request_line[2]
    pattern = r'\d+$'

# Use re.search to find the last number in the URL
    match = re.search(pattern, path)
    if match:
        number = match.group()
    else:
        number = 0

    response_content = ''
    status_code = 200

    if path =='/':
        response_content = "Hello World"
    elif path == "/home":
        response_content = "Home"
    elif path == "/contacts":
        response_content = "This is contacts page"
    elif path == "/about":
        response_content = "This is about page"
    elif path == "/products":
        response_content = product_names()
    elif path == f"/products/{number}":
        response_content = product_info(int(number))
    else:
        response_content = "404 Not Found"

    response = f"HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}"
    client_socket.send(response.encode('utf-8'))

    client_socket.close()

def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()