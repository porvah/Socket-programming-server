import os
import socket
import threading
DIR = os.path.join(os.getcwd(), "files")

def save_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)
    print(f"File saved as: {file_path}")

#function to get the name based on the type
def get_filename(base_name, content_type):
    if 'text/html' in content_type:
        extension = ".html"
    elif 'text/plain' in content_type:
        extension = ".txt"
    elif 'image/' in content_type:
        extension = ".jpeg"  
    else:
        raise ValueError("Unsupported content type")
    
    filename = f"{base_name}{extension}"
    return filename



def GET_handler(client_socket, request, file_path):
    
    if file_path == '/':
        return ("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: keep-alive\r\n\r\n"
                "<body><h1>This is the server home page</h1><p>Try to get and post files!!</p></body>").encode('utf-8')
    file_path = os.path.join(DIR, file_path.lstrip('/'))
    try:
        if file_path.endswith('.txt'):
            Ctype = "text/plain"
            rM = 'r'
            pass
        elif file_path.endswith('.html'):
            Ctype = 'text/html'
            rM = 'rb'
        else:
            Ctype = 'image/jpeg'
            rM = 'rb'

        file = open(file_path, rM)
        body = file.read()
        response = ("HTTP/1.1 200 OK \r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Content-Type: {Ctype}\r\n\r\n"
                    )
        body = body.encode('utf-8') if Ctype == 'text/plain' else body 
        return response.encode('utf-8')+body
    except Exception as e:
        print(e)
        return ("HTTP/1.1 404 Not Found\r\nContent-Length: 15\r\nContent-Type: text/plain\r\n\r\n"
                "File not found.").encode('utf-8')
    
    
def POST_handler(client_socket, request, file_path):
    # Parse headers and body
    header_data, _, body = request.partition(b"\r\n\r\n")
    # print("_ = " +_)
    # print("body = " + body)
    headers = header_data.decode("utf-8").split("\r\n")

    content_type = None
    for header in headers:
        if header.lower().startswith("content-type:"):
            content_type = header.split(":")[1].strip()
            break

    if not content_type:
        print("Failed to get file")
        response = "HTTP/1.1 400 Bad Request\r\n\r\nContent-Type header missing"
        return response.encode("utf-8")

    base_name = os.path.splitext(os.path.basename(file_path))[0] or "index"
    file_name = get_filename(base_name, content_type)

    save_directory = "posted_files"
    os.makedirs(save_directory, exist_ok=True)
    complete_file_path = os.path.join(save_directory, file_name)

    # Save the file
    save_file(complete_file_path, body)
    print(f"File saved as: {complete_file_path}")

    response = "HTTP/1.1 200 OK\r\n\r\n"
    return response.encode("utf-8")

def get_content_length(request):
    try:
        request_str = request.decode('utf-8' , errors='ignore')
    except Exception as e:
        print(f"Error: {e}")
        return None 

    lines = request_str.split('\r\n')
    for line in lines:
        if line.startswith('Content-Length:'):
            _, length = line.split(':', 1)
            return int(length.strip()) 


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
                    response = GET_handler(client_socket=client_socket, request=request2, file_path=file_path)
                elif method == "POST":
                    length = get_content_length(request)
                    if length > 1024:
                        request += client_socket.recv(length)
                        print(request)
                    response = POST_handler(client_socket=client_socket, request=request, file_path=file_path)
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
