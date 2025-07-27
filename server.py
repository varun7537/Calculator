import socket
import threading
import math

def calculate(expression):
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names['abs'] = abs
        allowed_names['round'] = round
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data.lower() == 'exit':
                print(f"Client {addr} disconnected.")
                break
            print(f"Received from {addr}: {data}")
            result = calculate(data)
            conn.sendall(str(result).encode())

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}...")
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
