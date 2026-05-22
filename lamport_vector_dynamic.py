def internal_event(process, vectors):
    vectors[process][process] += 1
    print(f"P{process+1} INTERNAL -> {vectors[process]}")

def send_event(process, vectors):
    vectors[process][process] += 1
    message_vector = vectors[process].copy()
    print(f"P{process+1} SEND -> {message_vector}")
    return message_vector

def receive_event(receiver, vectors, message_vector):
    for i in range(len(vectors)):
        vectors[receiver][i] = max(vectors[receiver][i], message_vector[i])

    vectors[receiver][receiver] += 1
    print(f"P{receiver+1} RECEIVE -> {vectors[receiver]}")

def display_vectors(vectors):
    print("\nCurrent Vector Clocks:")
    for i in range(len(vectors)):
        print(f"P{i+1} = {vectors[i]}")
    print("-" * 60)

def dynamic_vector_clock():
    n = int(input("Enter number of processes: "))
    vectors = [[0] * n for _ in range(n)]
    last_message = None

    while True:
        print("\n===== VECTOR CLOCK MENU =====")
        print("1. Internal Event")
        print("2. Send Message")
        print("3. Receive Message")
        print("4. Display Vector Clocks")
        print("5. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            p = int(input("Enter process number: ")) - 1
            internal_event(p, vectors)

        elif choice == 2:
            p = int(input("Enter sender process number: ")) - 1
            last_message = send_event(p, vectors)

        elif choice == 3:
            if last_message is None:
                print("No message available.")
                continue

            p = int(input("Enter receiver process number: ")) - 1
            receive_event(p, vectors, last_message)

        elif choice == 4:
            display_vectors(vectors)

        elif choice == 5:
            print("Exiting Vector Clock Simulation...")
            break

        else:
            print("Invalid choice!")

dynamic_vector_clock()
