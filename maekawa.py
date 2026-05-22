class Node:
    def __init__(self, node_id):
        self.id = node_id

        self.requesting = False
        self.in_cs = False
        self.replies_received = 0

        self.quorum = []
        self.nodes = []

        self.locked = False
        self.locked_by = None
        self.queue = []

    def set_nodes(self, nodes):
        self.nodes = nodes

    def set_quorum(self, quorum):
        self.quorum = quorum

    def request_cs(self):
        if self.in_cs:
            print(f"[Node {self.id}] already in CS!")
            return

        self.requesting = True
        self.replies_received = 0

        print(f"\n[Node {self.id}] REQUEST CS → Quorum: {self.quorum}")

        for q in self.quorum:
            if q != self.id:
                self.nodes[q].receive_request(self.id)

    def receive_request(self, sender_id):
        print(f"[Node {self.id}] received REQUEST from {sender_id}")

        if not self.locked:
            self.locked = True
            self.locked_by = sender_id
            print(f"[Node {self.id}] → REPLY to {sender_id}")
            self.nodes[sender_id].receive_reply(self.id)
        else:
            print(f"[Node {self.id}] → QUEUE {sender_id}")
            self.queue.append(sender_id)

    def receive_reply(self, sender_id):
        self.replies_received += 1
        print(f"[Node {self.id}] received REPLY from {sender_id}")

        if self.replies_received == len(self.quorum) - 1:
            self.enter_cs()

    def enter_cs(self):
        self.in_cs = True
        self.requesting = False
        print(f"\n>>> Node {self.id} ENTERS CS <<<\n")

    def exit_cs(self):
        print(f"\n[Node {self.id}] EXIT CS")

        self.in_cs = False

        for q in self.quorum:
            if q != self.id:
                self.nodes[q].receive_release(self.id)

    def receive_release(self, sender_id):
        print(f"[Node {self.id}] received RELEASE from {sender_id}")

        if self.locked_by == sender_id:
            if self.queue:
                next_node = self.queue.pop(0)
                self.locked_by = next_node
                print(f"[Node {self.id}] → REPLY to queued {next_node}")
                self.nodes[next_node].receive_reply(self.id)
            else:
                self.locked = False
                self.locked_by = None

def simulate():
    n = int(input("Enter number of nodes: "))
    nodes = [Node(i) for i in range(n)]

    for node in nodes:
        node.set_nodes(nodes)

    print("\nEnter quorum for each node (space-separated IDs):")
    for i in range(n):
        q = list(map(int, input(f"Node {i} quorum: ").split()))

        if i not in q:
            print(f"[Warning] Adding node {i} to its own quorum")
            q.append(i)

        nodes[i].set_quorum(q)

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
            print("\n--- STATUS ---")
            for node in nodes:
                print(f"Node {node.id} | InCS: {node.in_cs} | "
                      f"Locked: {node.locked} | Locked_by: {node.locked_by} | Queue: {node.queue}")
            print("----------------")

        elif choice == "4":
            break

        else:
            print("Invalid choice!")

simulate()
