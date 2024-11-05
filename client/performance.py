
import threading
from client import run_client

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


run_clients(10000)
