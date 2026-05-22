class Node:
    def __init__(self, i):
        self.id, self.alive, self.coordinator = i, True, None
        self.nodes, self.next = [], None

    def set_nodes(self, nodes): self.nodes = nodes
    def set_next(self, n): self.next = n

    def get_next_alive(self):
        c = self.next
        while not c.alive:
            c = c.next
        return c

    def start_election(self):
        if not self.alive:
            print(f"[Node {self.id}] is down."); return

        print(f"\n[Node {self.id}] starts ELECTION")
        self.get_next_alive().receive_token([self.id], self.id)

    def receive_token(self, token, init):
        if not self.alive: return

        print(f"[Node {self.id}] received TOKEN {token}")
        if self.id not in token:
            token.append(self.id)

        nxt = self.get_next_alive()
        if self.id == init:
            leader = max(token)
            print(f"\n[System] Leader is Node {leader}\n")
            self.announce_coordinator(leader)
        else:
            nxt.receive_token(token, init)

    def announce_coordinator(self, leader):
        self.coordinator = leader
        self.get_next_alive().receive_coordinator(leader, self.id)

    def receive_coordinator(self, leader, init):
        if not self.alive: return

        print(f"[Node {self.id}] → Coordinator is Node {leader}")
        self.coordinator = leader

        nxt = self.get_next_alive()
        if self.id != init:
            nxt.receive_coordinator(leader, init)

    def fail(self):
        self.alive = False
        print(f"[Node {self.id}] FAILED")

    def recover(self):
        self.alive = True
        print(f"[Node {self.id}] RECOVERED")

def simulate():
    n = int(input("Nodes: "))
    nodes = [Node(i) for i in range(n)]

    for i in range(n):
        nodes[i].set_nodes(nodes)
        nodes[i].set_next(nodes[(i + 1) % n])

    while True:
        print("\n1.Elect 2.Fail 3.Recover 4.Status 5.Exit")
        c = input("Choice: ")

        if c in "123":
            i = int(input(f"Node ID (0-{n-1}): "))
            if 0 <= i < n:
                if c == "1": nodes[i].start_election()
                elif c == "2": nodes[i].fail()
                else: nodes[i].recover()

        elif c == "4":
            print("\n--- STATUS ---")
            for n in nodes:
                print(f"Node {n.id} | Alive:{n.alive} | Coord:{n.coordinator}")
            print("----------------")

        elif c == "5":
            break
        else:
            print("Invalid!")

simulate()
