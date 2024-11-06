import socket
import time
from request_handlers import  client_get , handle_post , handle_get ,get_content_length
import argparse

"""
    this is the function for running the client
    - it begins by starting a timer
    - initiates a client socket and requests a connection with the server
    - after that it opens the input.txt file and begins parsing and executing commands
      based on their content and sends them to the appropriate handler
    - in the end the timer is stopped and connection is closed ending the program along with it
"""
def run_client(file_name , server_ip , port_number):  
    start_time = time.time()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    client.connect((server_ip, port_number))

    try:
        with open(file_name, 'r') as file:
            for command_line in file:
                command = command_line.strip().split()
                if not command:
                    continue
                print(command)
                command_request = command[0]
                file_path = command[1]
                host_name = command[2]
                port_number = int(command[3]) if len(command) > 3 else 80

                if command_request == "client_get":
                    #send a request
                    msg = client_get(file_path, host_name, port_number)
                    client.send(msg.encode("utf-8"))
                    response = client.recv(1024)
                    #check the content length of the response
                    length = get_content_length(response)
                    if length > 1024:
                        response += client.recv(length)

                    #handle the response
                    handle_get(response , file_path)
                    
                elif command_request == "client_post":
                    msg = handle_post(file_path , host_name , port_number)
                    
                    client.send(msg)
                    response = client.recv(1024)
                else:
                    print("Invalid command")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        end_time = time.time()
        client.close()
        print("Connection to server closed")
        print("time= " +str(end_time - start_time))
        return end_time - start_time

# This is the code for parsing arguments from the terminal
parser = argparse.ArgumentParser(description="Parser for port argument")

parser.add_argument("ip", type=str, default='127.0.0.1', help="hostname") 
parser.add_argument("port", type=int, help="Server port")  

args = parser.parse_args()

run_client('input.txt' , args.ip , args.port)
