class Node:
    def __init__(self, i):
        self.id, self.alive, self.coordinator, self.nodes = i, True, None, []

    def set_nodes(self, nodes):
        self.nodes = nodes

    def start_election(self):
        if not self.alive:
            print(f"[Node {self.id}] is down.")
            return

        print(f"\n[Node {self.id}] starts ELECTION")
        higher = [n for n in self.nodes if n.id > self.id and n.alive]

        if not higher:
            return self.become_coordinator()

        res = []
        for n in higher:
            print(f"[Node {self.id}] → ELECTION to Node {n.id}")
            if n.receive_election(self.id):
                res.append(n.id)

        if res:
            print(f"[Node {self.id}] OK from {res} → waiting...")
        else:
            self.become_coordinator()

    def receive_election(self, sender):
        if not self.alive:
            return False

        print(f"[Node {self.id}] got ELECTION from {sender}")
        print(f"[Node {self.id}] → OK to Node {sender}")
        self.start_election()
        return True

    def become_coordinator(self):
        print(f"\n>>> Node {self.id} is COORDINATOR <<<\n")
        self.coordinator = self.id
        for n in self.nodes:
            if n.id != self.id and n.alive:
                n.receive_coordinator(self.id)

    def receive_coordinator(self, leader):
        print(f"[Node {self.id}] → Coordinator is {leader}")
        self.coordinator = leader

    def fail(self):
        self.alive = False
        print(f"[Node {self.id}] FAILED")

    def recover(self):
        self.alive = True
        print(f"[Node {self.id}] RECOVERED")
        self.start_election()

def simulate():
    n = int(input("Nodes: "))
    nodes = [Node(i) for i in range(n)]
    for node in nodes:
        node.set_nodes(nodes)

    nodes[-1].become_coordinator()

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
            for n in nodes:
                print(f"Node {n.id} | Alive:{n.alive} | Coord:{n.coordinator}")

        elif c == "5":
            break

        else:
            print("Invalid!")

simulate()
