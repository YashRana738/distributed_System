import queue
import threading
import time

process_queue = queue.Queue()
start_time_global = time.time()

class Process:
    def __init__(self, pid, arrival_time, burst_time, node):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.node = node

        self.start_time = None
        self.completion_time = None
        self.turnaround_time = None
        self.waiting_time = None
        self.response_time = None

def node_send_processes(node_id, processes):
    for p in processes:
        time.sleep(p.arrival_time)
        print(f"Node {node_id} sending Process {p.pid}")
        process_queue.put(p)

def round_robin_scheduler(total_processes, time_quantum):
    completed = 0
    results = []

    while completed < total_processes:
        if not process_queue.empty():
            process = process_queue.get()

            current_time = time.time() - start_time_global

            if process.start_time is None:
                process.start_time = current_time
                process.response_time = process.start_time - process.arrival_time

            execute_time = min(time_quantum, process.remaining_time)

            print(f"\nExecuting Process {process.pid} (Node {process.node}) for {execute_time}")

            time.sleep(execute_time)

            process.remaining_time -= execute_time

            if process.remaining_time > 0:
                print(f"Process {process.pid} remaining: {process.remaining_time} → re-queued")
                process_queue.put(process)
            else:
                process.completion_time = time.time() - start_time_global

                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time

                print(f"Process {process.pid} completed\n")

                results.append(process)
                completed += 1

    return results

time_quantum = float(input("Enter Time Quantum: "))

num_nodes = int(input("Enter number of nodes: "))
all_threads = []
total_processes = 0

for n in range(1, num_nodes + 1):
    num_processes = int(input(f"\nEnter number of processes for Node {n}: "))
    processes = []

    for i in range(num_processes):
        pid = int(input("Enter PID: "))
        at = float(input("Enter Arrival Time: "))
        bt = float(input("Enter Burst Time: "))

        processes.append(Process(pid, at, bt, n))

    total_processes += num_processes

    t = threading.Thread(target=node_send_processes, args=(n, processes))
    all_threads.append(t)

for t in all_threads:
    t.start()

results = round_robin_scheduler(total_processes, time_quantum)

for t in all_threads:
    t.join()

print("\nFinal Results:\n")
print("PID\tAT\tBT\tCT\tTAT\tWT\tRT")

for p in results:
    print(f"{p.pid}\t{p.arrival_time:.2f}\t{p.burst_time:.2f}\t"
          f"{p.completion_time:.2f}\t{p.turnaround_time:.2f}\t"
          f"{p.waiting_time:.2f}\t{p.response_time:.2f}")
