import socket
import threading
from handlers import GET_handler, get_content_length, POST_handler


def handle_client(client_socket, addr):
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024)
            if request:
                request2 = request.decode('utf-8', errors='ignore')
                command = request2.splitlines()[0]
                method, file_path, _ = command.split()
                response = ''
                if method == "GET":
                    response = GET_handler(request=request2, file_path=file_path)
                elif method == "POST":
                    length = get_content_length(request)
                    if length > 1024:
                        request += client_socket.recv(length)
                    response = POST_handler(request=request, file_path=file_path)
                else:
                    response = "HTTP/1.1 404 Not Found\r\n".encode("utf-8")
                # convert and send accept response to the client
                
                #response += "\r\n"
                client_socket.send(response)
            else:
                break
    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server():
    server_ip = args.ip  # server hostname or IP address
    port = args.port  # server port number
    # create a socket object
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connections
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            # accept a client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

import argparse

parser = argparse.ArgumentParser(description="Parser for port argument")

parser.add_argument("port", type=int, help="Server port")  
parser.add_argument("--ip", type=str, default='127.0.0.1', help="hostname")  #optional argument

args = parser.parse_args()
run_server()
