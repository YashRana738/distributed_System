class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.holder = None
        self.request_queue = []
        self.has_token = False
        self.using_cs = False

    def request_cs(self):
        print(f"\nNode {self.id} requests Critical Section")

        if self not in self.request_queue:
            self.request_queue.append(self)

        self.send_request()
        self.process_queue()

    def send_request(self):
        current = self

        while not current.has_token:
            parent = current.holder
            print(f"REQUEST: Node {current.id} --> Node {parent.id}")

            if current not in parent.request_queue:
                parent.request_queue.append(current)

            current = parent

        current.process_queue()

    def process_queue(self):
        if self.has_token and self.request_queue:
            next_node = self.request_queue.pop(0)

            if next_node == self:
                self.enter_cs()
            else:
                print(f"TOKEN: Node {self.id} --> Node {next_node.id}")

                self.has_token = False
                next_node.has_token = True

                self.holder = next_node
                next_node.holder = next_node

                next_node.process_queue()

    def enter_cs(self):
        self.using_cs = True
        print(f"*** Node {self.id} ENTERS Critical Section ***")

    def release_cs(self):
        if self.using_cs:
            print(f"*** Node {self.id} RELEASES Critical Section ***")
            self.using_cs = False
            self.process_queue()

n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)
n5 = Node(5)

n2.holder = n1
n3.holder = n1
n4.holder = n2
n5.holder = n2

n1.has_token = True
n1.holder = n1

nodes = {
    1: n1,
    2: n2,
    3: n3,
    4: n4,
    5: n5
}

while True:
    req = int(input("\nEnter requesting node (1-5, -1 to exit): "))

    if req == -1:
        print("Simulation ended.")
        break

    if req not in nodes:
        print("Invalid node!")
        continue

    nodes[req].request_cs()
    nodes[req].release_cs()
