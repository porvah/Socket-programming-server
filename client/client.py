import socket
import time
from request_handlers import  client_get , client_post , handle_get ,get_content_length
import threading

def run_client(file_name):  
    start_time = time.time()
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    server_port = 8000  
    # Establish connection with the server
    client.connect((server_ip, server_port))

    try:
        with open(file_name, 'r') as file:
            for command_line in file:
                command = command_line.strip().split()
                print(command)
                if not command:
                    continue

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
                    client_post(file_path, host_name, port_number)
                else:
                    print("Invalid command")
        end_time = time.time()

        return end_time - start_time

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close client socket (connection to the server)
        client.close()
        print("Connection to server closed")


#for performance evaluation
def run_clients(num_of_clients):
    threads = []
    times = []
    for i in range(num_of_clients):
        print("thread " + str(i) + " starts")
        thread = threading.Thread(target=lambda: times.append(run_client("input.txt")))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    avg_delay = sum(times) / len(times) if times else 0
    print(f"Average delay with {num_of_clients} clients: {avg_delay:.4f} seconds")

    for time in times:
        print(time)

run_clients(7)

