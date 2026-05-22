class Token:
    def __init__(self, n):
        self.LN = [0] * n
        self.Q = []

class Node:
    def __init__(self, node_id, n):
        self.id = node_id
        self.n = n
        self.RN = [0] * n
        self.has_token = False
        self.token = None
        self.in_cs = False

    def show_state(self):
        print(f"\nNode {self.id + 1} RN = {self.RN}")
        if self.has_token:
            print(f"Token LN = {self.token.LN}")
            print(f"Token Queue = {[x + 1 for x in self.token.Q]}")
            print(f"Node {self.id + 1} HOLDS TOKEN")
        if self.in_cs:
            print(f"Node {self.id + 1} is IN CS")

    def request_cs(self, nodes):
        print(f"\nNode {self.id + 1} requests Critical Section")

        if self.has_token and not self.in_cs:
            self.enter_cs()
            return

        self.RN[self.id] += 1
        req_no = self.RN[self.id]
        print(f"Updated RN[{self.id + 1}] = {req_no}")

        for node in nodes:
            if node.id != self.id:
                print(f"REQUEST({self.id + 1}, {req_no}): {self.id + 1} --> {node.id + 1}")
                node.RN[self.id] = max(node.RN[self.id], req_no)

        for node in nodes:
            if node.has_token:

                if not node.in_cs:
                    if node.token.LN[self.id] + 1 == req_no:
                        print(f"TOKEN: Node {node.id + 1} --> Node {self.id + 1}")

                        self.has_token = True
                        self.token = node.token
                        node.has_token = False
                        node.token = None

                        self.enter_cs()
                        return
                else:
                    if self.id not in node.token.Q:
                        node.token.Q.append(self.id)

    def enter_cs(self):
        self.in_cs = True
        print(f"\n*** Node {self.id + 1} ENTERS Critical Section ***")

    def release_cs(self, nodes):
        if not self.in_cs:
            print("This node is not in CS")
            return

        print(f"\n*** Node {self.id + 1} RELEASES Critical Section ***")
        self.in_cs = False

        self.token.LN[self.id] = self.RN[self.id]

        print(f"Updated LN = {self.token.LN}")
        print(f"Updated Queue = {[x + 1 for x in self.token.Q]}")

        if self.token.Q:
            next_id = self.token.Q.pop(0)

            print(f"TOKEN: Node {self.id + 1} --> Node {next_id + 1}")

            receiver = nodes[next_id]
            receiver.has_token = True
            receiver.token = self.token

            self.has_token = False
            self.token = None

            receiver.enter_cs()

N = 5
nodes = [Node(i, N) for i in range(N)]

nodes[0].has_token = True
nodes[0].token = Token(N)

while True:
    print("\n1. Request CS")
    print("2. Release CS")
    print("3. Show All States")
    print("4. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        req = int(input("Enter requesting node (1-5): "))
        nodes[req - 1].request_cs(nodes)

    elif choice == 2:
        req = int(input("Enter node releasing CS (1-5): "))
        nodes[req - 1].release_cs(nodes)

    elif choice == 3:
        for node in nodes:
            node.show_state()

    elif choice == 4:
        break
