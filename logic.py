def max_value(a, b):
    if a > b:
        return a
    return b

def lamport_logical_clock():
    n = int(input("Enter number of processes: "))

    events = []
    for i in range(n):
        e = int(input(f"Enter number of events in Process P{i + 1}: "))
        events.append(e)

    clocks = []
    for i in range(n):
        row = []
        for j in range(events[i]):
            row.append(0)
        clocks.append(row)

    for i in range(n):
        for j in range(events[i]):
            if j == 0:
                clocks[i][j] = 1
            else:
                clocks[i][j] = clocks[i][j - 1] + 1

    m = int(input("Enter number of message relations: "))

    for _ in range(m):
        sender = int(input("Sender Process number: ")) - 1
        send_event = int(input("Sender Event number: ")) - 1
        receiver = int(input("Receiver Process number: ")) - 1
        receive_event = int(input("Receiver Event number: ")) - 1

        clocks[receiver][receive_event] = max_value(
            clocks[receiver][receive_event],
            clocks[sender][send_event] + 1
        )

        for k in range(receive_event + 1, events[receiver]):
            clocks[receiver][k] = clocks[receiver][k - 1] + 1

    print("\nLamport Logical Clock Values:")
    for i in range(n):
        print(f"Process P{i + 1}: ", end="")
        for j in range(events[i]):
            print(clocks[i][j], end=" ")
        print()
lamport_logical_clock()
