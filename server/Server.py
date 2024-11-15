import socket
import threading
from handlers import GET_handler, get_content_length, POST_handler
import argparse
# Global variables
"""
    defTimeout is the timeout for a single threaded server
    threadsCount is to keep track of current open threads
    count_lock is a lock to protect threadsCount from race condition
    max_thread_count is a counter for the maximum concurrent threads in the server
"""
defTimout = 20.0
threadsCount = 1
count_lock = threading.Lock()
max_thread_count = 1

"""
    handle_client() -> 
        increment thread count
        continues to recieve from the socket
        puts a timout on the socket depending on the number of live sockets in the server.
        parsers request and forwards it to the appropriate handler (GET or POST)
        handles invalid requests and catches timout by closing connection
"""
def handle_client(client_socket, addr):
    global threadsCount
    global max_thread_count
    with count_lock:  # Ensure exclusive access
        threadsCount += 1
        max_thread_count = max(max_thread_count, threadsCount)
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024)
            if request:
                client_socket.settimeout(defTimout/threadsCount)
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
    except socket.timeout:
        print("connection timedout")
    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        with count_lock:
            threadsCount-= 1
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")
        print("maximum concurrent threads = "+ str(max_thread_count-1))


"""
    run_server()->
        gets server ip and port from arguments
        creates server port and listens for connection requests
        any new request is handled on a seperate thread using the handler (handle_client)
"""
def run_server():
    server_ip = args.ip  # server hostname or IP address
    port = args.port  # server port number
    
    try:
        # server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connections
        server.listen()
        print(f"Listening on {server_ip}:{port}")
        
        while True:
            # accept a client connection
            client_socket, addr = server.accept()
            client_socket.settimeout(defTimout/threadsCount)
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
            # this line is for single threaded server
            # handle_client(client_socket=client_socket, addr=addr)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


# logic for parsing terminal arguments
parser = argparse.ArgumentParser(description="Parser for port argument")

parser.add_argument("port", type=int, help="Server port")  
parser.add_argument("--ip", type=str, default='127.0.0.1', help="hostname")  #optional argument

args = parser.parse_args()
run_server()
