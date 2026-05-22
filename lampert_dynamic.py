def internal_event(process_name, event_name, clock):
    clock += 1
    print(f"{process_name} -> {event_name} -> INTERNAL EVENT -> Clock = {clock}")
    return clock

def send_event(sender_name, event_name, clock):
    clock += 1
    timestamp = clock
    print(f"{sender_name} -> {event_name} -> SEND EVENT -> Timestamp = {timestamp}")
    return clock, timestamp

def receive_event(receiver_name, event_name, clock, received_timestamp):
    old_clock = clock
    clock = max(clock, received_timestamp) + 1
    print(
        f"{receiver_name} -> {event_name} -> RECEIVE EVENT -> "
        f"max({old_clock}, {received_timestamp}) + 1 = {clock}"
    )
    return clock

def display_clocks(clocks):
    print("\nCurrent Clock Values:")
    for i in range(len(clocks)):
        print(f"P{i+1} = {clocks[i]}")
    print("-" * 60)

def lamport_menu():
    n = int(input("Enter number of processes: "))
    clocks = [0] * n
    event_counter = 1
    last_sent_timestamp = None

    while True:
        print("\n===== LAMPORT LOGICAL CLOCK MENU =====")
        print("1. Internal Event")
        print("2. Send Message")
        print("3. Receive Message")
        print("4. Display Clocks")
        print("5. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            p = int(input("Enter process number: ")) - 1
            event_name = f"e{event_counter}"
            clocks[p] = internal_event(f"P{p+1}", event_name, clocks[p])
            event_counter += 1

        elif choice == 2:
            p = int(input("Enter sender process number: ")) - 1
            event_name = f"e{event_counter}"
            clocks[p], last_sent_timestamp = send_event(
                f"P{p+1}", event_name, clocks[p]
            )
            event_counter += 1

        elif choice == 3:
            if last_sent_timestamp is None:
                print("No message available to receive.")
                continue

            p = int(input("Enter receiver process number: ")) - 1
            event_name = f"e{event_counter}"
            clocks[p] = receive_event(
                f"P{p+1}", event_name, clocks[p], last_sent_timestamp
            )
            event_counter += 1

        elif choice == 4:
            display_clocks(clocks)

        elif choice == 5:
            print("\nExiting Lamport Logical Clock Simulation...")
            break

        else:
            print("Invalid choice! Please try again.")

lamport_menu()
