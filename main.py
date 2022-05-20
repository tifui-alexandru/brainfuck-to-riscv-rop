from bf_parser import *

p = BF_Parser("><")

offset = ""
offset = bytes(input("Please provide offset until stack smash:\n"), 'utf-8')

print(offset + p.parse())