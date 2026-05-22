def internal_event(process, vc):
    vc[process] += 1
    print(f"P{process+1} INTERNAL -> {vc}")
    return vc

def send_event(process, vc):
    vc[process] += 1
    message_vector = vc.copy()
    print(f"P{process+1} SEND -> {message_vector}")
    return vc, message_vector

def receive_event(process, vc, received_vector):
    for i in range(len(vc)):
        vc[i] = max(vc[i], received_vector[i])
    vc[process] += 1
    print(f"P{process+1} RECEIVE -> {vc}")
    return vc

def static_vector_clock():
    n = 3
    P1 = [0] * n
    P2 = [0] * n
    P3 = [0] * n

    print("Initial State")
    print("P1:", P1)
    print("P2:", P2)
    print("P3:", P3)
    print("-" * 50)

    P1 = internal_event(0, P1)
    P1 = internal_event(0, P1)

    P1, msg1 = send_event(0, P1)

    P2 = receive_event(1, P2, msg1)

    P2 = internal_event(1, P2)

    P2, msg2 = send_event(1, P2)

    P3 = receive_event(2, P3, msg2)

    print("-" * 50)
    print("Final Vector Clocks")
    print("P1:", P1)
    print("P2:", P2)
    print("P3:", P3)

static_vector_clock()
