def internal_event(process_name, event_name, clock):

    clock += 1
    print(f"{process_name} -> {event_name} -> INTERNAL EVENT -> Clock = {clock}")
    return clock

def send_event(sender_name, event_name, clock):

    clock += 1
    timestamp = clock
    print(
        f"{sender_name} -> {event_name} -> SEND EVENT -> "
        f"Message timestamp = {timestamp}"
    )
    return clock, timestamp

def receive_event(receiver_name, event_name, clock, received_timestamp):

    old_clock = clock
    clock = max(clock, received_timestamp) + 1
    print(
        f"{receiver_name} -> {event_name} -> RECEIVE EVENT -> "
        f"max({old_clock}, {received_timestamp}) + 1 = {clock}"
    )
    return clock

def display_clocks(P1, P2, P3):
    print(f"Current Clocks => P1: {P1}, P2: {P2}, P3: {P3}")
    print("-" * 70)

def lamport_named_event_simulation():
    P1, P2, P3 = 0, 0, 0

    print("LAMPORT LOGICAL CLOCK WITH NAMED EVENTS")

    display_clocks(P1, P2, P3)

    P1 = internal_event("P1", "e1", P1)
    display_clocks(P1, P2, P3)

    P1 = internal_event("P1", "e2", P1)
    display_clocks(P1, P2, P3)

    P1, msg1 = send_event("P1", "e3", P1)
    display_clocks(P1, P2, P3)

    P2 = receive_event("P2", "e4", P2, msg1)
    display_clocks(P1, P2, P3)

    P2 = internal_event("P2", "e5", P2)
    display_clocks(P1, P2, P3)

    P2 = internal_event("P2", "e6", P2)
    display_clocks(P1, P2, P3)

    P2, msg2 = send_event("P2", "e7", P2)
    display_clocks(P1, P2, P3)

    P3 = receive_event("P3", "e8", P3, msg2)
    display_clocks(P1, P2, P3)

    P3 = internal_event("P3", "e9", P3)
    display_clocks(P1, P2, P3)

    P3 = internal_event("P3", "e10", P3)
    display_clocks(P1, P2, P3)

    P3, msg3 = send_event("P3", "e11", P3)
    display_clocks(P1, P2, P3)

    P1 = receive_event("P1", "e12", P1, msg3)
    display_clocks(P1, P2, P3)

    print("FINAL CLOCK VALUES")

    display_clocks(P1, P2, P3)

lamport_named_event_simulation()
