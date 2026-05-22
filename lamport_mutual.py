class Node:
    def __init__(self, node_id, total_nodes):
        self.id = node_id
        self.total_nodes = total_nodes

        self.clock = 0
        self.requesting = False
        self.in_cs = False

        self.timestamp = None
        self.replies_received = 0

        self.request_queue = []

        self.nodes = []

    def set_nodes(self, nodes):
        self.nodes = nodes

    def increment_clock(self):
        self.clock += 1

    def update_clock(self, ts):
        self.clock = max(self.clock, ts) + 1

    def request_cs(self):
        if self.in_cs:
            print(f"[Node {self.id}] already in CS!")
            return

        self.increment_clock()
        self.timestamp = self.clock
        self.requesting = True
        self.replies_received = 0

        self.request_queue.append((self.timestamp, self.id))
        self.request_queue.sort()

        print(f"\n[Node {self.id}] REQUEST CS at time {self.timestamp}")

        for node in self.nodes:
            if node.id != self.id:
                node.receive_request(self.id, self.timestamp)

    def receive_request(self, sender_id, sender_ts):
        self.update_clock(sender_ts)

        print(f"[Node {self.id}] received REQUEST from {sender_id}")

        self.request_queue.append((sender_ts, sender_id))
        self.request_queue.sort()

        self.nodes[sender_id].receive_reply(self.id, self.clock)
        print(f"[Node {self.id}] → REPLY to {sender_id}")

    def receive_reply(self, sender_id, sender_ts):
        self.update_clock(sender_ts)

        self.replies_received += 1
        print(f"[Node {self.id}] received REPLY from {sender_id}")

        self.try_enter_cs()

    def try_enter_cs(self):
        if (self.replies_received == self.total_nodes - 1 and
            self.request_queue and
            self.request_queue[0] == (self.timestamp, self.id)):

            self.enter_cs()

    def enter_cs(self):
        self.in_cs = True
        self.requesting = False
        print(f"\n>>> Node {self.id} ENTERS CS <<<\n")

    def exit_cs(self):
        print(f"\n[Node {self.id}] EXIT CS")

        self.in_cs = False

        if (self.timestamp, self.id) in self.request_queue:
            self.request_queue.remove((self.timestamp, self.id))

        for node in self.nodes:
            if node.id != self.id:
                node.receive_release(self.id, self.clock)

        self.timestamp = None

    def receive_release(self, sender_id, sender_ts):
        self.update_clock(sender_ts)

        print(f"[Node {self.id}] received RELEASE from {sender_id}")

        self.request_queue = [
            req for req in self.request_queue if req[1] != sender_id
        ]

        self.try_enter_cs()

def simulate():
    n = int(input("Enter number of nodes: "))
    nodes = [Node(i, n) for i in range(n)]

    for node in nodes:
        node.set_nodes(nodes)

    while True:
        print("\nOptions:")
        print("1. Request CS")
        print("2. Exit CS (Auto)")
        print("3. Show Status")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            node_id = int(input(f"Enter node ID (0 to {n-1}): "))
            if 0 <= node_id < n:
                nodes[node_id].request_cs()
            else:
                print("Invalid node!")

        elif choice == "2":
            exited = False
            for node in nodes:
                if node.in_cs:
                    print(f"\n[System] Node {node.id} exiting CS...")
                    node.exit_cs()
                    exited = True
                    break

            if not exited:
                print("[System] No node in CS!")

        elif choice == "3":
            print("\n--- SYSTEM STATUS ---")
            for node in nodes:
                print(f"Node {node.id} | Clock: {node.clock} | "
                      f"InCS: {node.in_cs} | Queue: {node.request_queue}")
            print("----------------------")

        elif choice == "4":
            break

        else:
            print("Invalid choice!")

simulate()
