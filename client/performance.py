
import argparse
from ast import arg
import threading
from client import run_client
# code for performance evaluation 
# it runs the client on multiple threads and computes the average delay
def run_clients(num_of_clients):
    threads = []
    times = []
    for i in range(num_of_clients):
        print("thread " + str(i) + " starts")
        thread = threading.Thread(target=lambda: times.append(run_client("input.txt" ,args.ip , args.port)))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    avg_delay = sum(times) / len(times) if times else 0
    print(f"Average delay with {num_of_clients} clients: {avg_delay:.4f} seconds")


parser = argparse.ArgumentParser(description="Parser for port argument")

parser.add_argument("ip", type=str, default='127.0.0.1', help="hostname") 
parser.add_argument("port", type=int, help="Server port")  

args = parser.parse_args()

run_clients(10000)