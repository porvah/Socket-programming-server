import os
import socket
import threading
DIR = os.path.join(os.getcwd(), "files")
def GET_handler(client_socket, request, file_path):
    print(file_path)
    if file_path == '/':
        return ("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: keep-alive\r\n\r\n"
                "<body><h1>This is the server home page</h1><p>Try to get and post files!!</p></body>").encode('utf-8')
    print("here")
    file_path = os.path.join(DIR, file_path.lstrip('/'))
    print(file_path)
    try:
        Ctype = "text/plain" if file_path.endswith('.txt') else 'text/html' if file_path.endswith('.html') else 'image/jpeg'
        print("file_path")
        file = open(file_path, 'rb')
        body = file.read()
        response = ("HTTP/1.1 200 OK \r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Content-Type: {Ctype}\r\n\r\n"
                    )
        return response.encode('utf-8')+body
    except Exception as e:
        print(e)
        return ("HTTP/1.1 404 Not Found\r\nContent-Length: 15\r\nContent-Type: text/plain\r\n\r\n"
                "File not found.").encode('utf-8')
    
    pass
def POST_handler(client_socket, request, file_path):
    pass

def handle_client(client_socket, addr):
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            print(f"Received: {request}")
            command = request.splitlines()[0]
            print(command)
            method, file_path, _ = command.split()
            response = ''
            if method == "GET":
                response = GET_handler(client_socket=client_socket, request=request, file_path=file_path)
                print(response)
            elif method == "POST":
                response = POST_handler(client_socket=client_socket, request=request, file_path=file_path)
            else:
                response = "HTTP/1.1 404 Not Found\r\n".encode("utf-8")
            # convert and send accept response to the client
            
            #response += "\r\n"
            client_socket.send(response)
    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server():
    server_ip = "127.0.0.1"  # server hostname or IP address
    port = 8000  # server port number
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


run_server()
