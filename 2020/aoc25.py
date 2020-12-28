with open("input/input25.txt") as f:
    content = f.read().splitlines()

card_key = int(content[0])
door_key = int(content[1])
subject_number = 7


def find_loop_size(the_subject_number, the_key):
    curr_loop_size = 0
    curr = 1
    while curr != the_key:
        curr *= the_subject_number
        curr = curr % 20201227
        curr_loop_size += 1
    return curr_loop_size


def apply_loop_size(the_loop_size, the_subject):
    transformed = 1
    for i in range(0, the_loop_size):
        transformed = (transformed * the_subject) % 20201227
    return transformed


card_loop_size = find_loop_size(subject_number, card_key)
door_loop_size = find_loop_size(subject_number, door_key)

encryption_key_1 = apply_loop_size(card_loop_size, door_key)
encryption_key_2 = apply_loop_size(door_loop_size, card_key)
assert encryption_key_1 == encryption_key_2

print("Solution 1: the encryption key is {}".format(encryption_key_1))
