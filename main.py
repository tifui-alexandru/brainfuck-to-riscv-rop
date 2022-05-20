from bf_parser import *

p = BF_Parser("><")

offset = b"A" * 23 # offset until stack smash ; added for debugging

print(offset + p.parse())