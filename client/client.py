import socket
from client.request_handlers import  client_get , client_post

def run_client(file_name):
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    server_port = 8000  
    # Establish connection with the server
    client.connect((server_ip, server_port))

    try:
        with open(file_name, 'r') as file:
            for command_line in file:
                command = command_line.strip().split()  # Read and strip whitespace

                if not command:  # Skip empty lines
                    continue

                command_request = command[0]
                file_path = command[1]
                host_name = command[2]
                port_number = int(command[3]) if len(command) > 3 else 80

                if command_request == "client_get":
                    client_get(file_path, host_name, port_number)
                elif command_request == "client_post":
                    client_post(file_path, host_name, port_number)
                else:
                    print("Invalid command")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close client socket (connection to the server)
        client.close()
        print("Connection to server closed")


run_client("client/input.txt")
