from bf_parser.jop_gadgets.increment_a3 import *
from bf_parser.jop_gadgets.increment_s0 import *
from bf_parser.jop_gadgets.initialize_a2 import *
from bf_parser.jop_gadgets.initialize_a3 import *
from bf_parser.jop_gadgets.initialize_a3_a7 import *
from bf_parser.jop_gadgets.store_s0 import *
from bf_parser.jop_gadgets.load_s0 import *
from bf_parser.jop_gadgets.li_a1_0 import *
from bf_parser.jop_gadgets.mov_s0_a0 import *
from bf_parser.jop_gadgets.init_args import *
from bf_parser.jop_gadgets.init_a5 import *

from bf_parser.rop_gadgets.copy_a3 import *
from bf_parser.rop_gadgets.restore_a3 import *
from bf_parser.rop_gadgets.mov_a0_s0 import *
from bf_parser.rop_gadgets.and_a3_s0 import *
from bf_parser.rop_gadgets.charger import *
from bf_parser.rop_gadgets.store_a0 import*
from bf_parser.rop_gadgets.ecall import *
from bf_parser.rop_gadgets.move_sp import *
from bf_parser.rop_gadgets.pop_s0 import *
from bf_parser.rop_gadgets.mov_a0_a4 import *
from bf_parser.rop_gadgets.mov_a4_a3 import *
from bf_parser.rop_gadgets.beqz_a0 import *
from bf_parser.rop_gadgets.add_a0_s0 import *

class BF_Parser():
    def __init__(self, bf_code):
        # trim bf code (only valid instruction make into the parsable code)
        self.__bf_code = [ch for ch in bf_code if ch in {'>', '<', '.', ',', '+', '-', '[', ']'}]

        self.__addr_mask = 0x3fffffffff # to restore the address using only the lower 32 bits
        
        # key   -> opening bracket's position
        # value -> closing bracket's position
        self.__brackets = dict()

        # rop gadget objects
        self.__charger    = Charger()
        self.__copy_a3    = CopyA3()
        self.__restore_a3 = RestoreA3()
        self.__mov_a0_s0  = MovA0_S0()
        self.__and_a3_s0  = AndA3_S0()
        self.__store_a0   = StoreA0()
        self.__ecall      = Ecall()
        self.__move_sp    = MoveSP()
        self.__pop_s0     = PopS0()
        self.__mov_a4_a3  = MOVA4_A3()
        self.__mov_a0_a4  = MOVA0_A4()
        self.__beqz_a0    = Beqz_a0()
        self.__add_a0_s0  = Add_A0_S0()

        # jop gadget objects
        self.__init_a3    = InitializeA3()
        self.__inc_a3     = IncrementA3()
        self.__load_s0    = LoadS0()
        self.__inc_s0     = IncrementS0()
        self.__store_s0   = StoreS0()
        self.__init_a7    = InitializeA5_A7()
        self.__init_args  = InitializeArgs()
        self.__mov_s0_a0  = MovS0_A0()

    def get_entry_point(self):
        return self.__charger.print_vaddr() # charger address that overrides $ra

    def __get_instruction_len(self, instruction):
        if instruction == '>' or instruction == '<':
            return self.__charger.get_frame_size()

        elif instruction == '+' or instruction == '-':
            return 3 *  self.__charger.get_frame_size() + \
                   self.__copy_a3.get_frame_size() + \
                   self.__restore_a3.get_frame_size() + \
                   self.__mov_a0_s0.get_frame_size() + \
                   self.__and_a3_s0.get_frame_size() + \
                   self.__store_a0.get_frame_size() + \
                   self.__mov_a0_a4.get_frame_size() + \
                   self.__mov_a4_a3.get_frame_size()

        elif instruction == '.' or instruction == ',':
            return 2 * self.__charger.get_frame_size() + \
                   self.__ecall.get_frame_size() + \
                   self.__copy_a3.get_frame_size() + \
                   self.__restore_a3.get_frame_size() + \
                   self.__and_a3_s0.get_frame_size()

        elif instruction == '[' or instruction == ']':
            return self.__pop_s0.get_frame_size() + \
                   self.__move_sp.get_frame_size() + \
                   self.__copy_a3.get_frame_size() + \
                   self.__mov_a4_a3.get_frame_size() + \
                   self.__mov_a0_a4.get_frame_size() + \
                   2 * self.__charger.get_frame_size() + \
                   self.__mov_a0_s0.get_frame_size() + \
                   self.__beqz_a0.get_frame_size() + \
                   self.__add_a0_s0.get_frame_size()

    def __parse_no_jumps(self, start_section, end_section, sp):
        if start_section >= end_section:
            return sp, b""

        # parse brainfuck code with no conditional jumps

        # provide frame for unconditional jump to this address
        rop_chain = self.__pop_s0.construct_frame(ra=self.__move_sp.get_vaddr(), \
                                                  s0=sp + self.__pop_s0.get_frame_size() + 0x50 \
                                                  )

        rop_chain += self.__move_sp.construct_frame(ra=self.__charger.get_vaddr())
        new_sp = sp + self.__pop_s0.get_frame_size() + self.__move_sp.get_frame_size()

        for idx, instruction in enumerate(self.__bf_code[start_section : end_section]):
            next_gadget_addr = self.__charger.get_vaddr()
            if idx == end_section - start_section - 1:
                next_gadget_addr = self.__pop_s0.get_vaddr()

            if instruction == '>' or instruction == '<':
                increment = 0x8 if instruction == '>' else -0x8

                # construct rop chain
                rop_chain += self.__charger.construct_frame(ra=self.__inc_a3.get_vaddr(), \
                                                            s1=increment, \
                                                            s4=next_gadget_addr \
                                                            )

                # advance sp
                new_sp += self.__get_instruction_len(instruction)

            elif instruction == '+' or instruction == '-':
                increment = 1 if instruction == '+' else -1

                backup_addr = new_sp + \
                              3 * self.__charger.get_frame_size() + \
                              self.__copy_a3.get_frame_size() + \
                              self.__mov_a0_s0.get_frame_size() + \
                              self.__restore_a3.get_frame_size() + \
                              self.__mov_a4_a3.get_frame_size() + \
                              self.__mov_a0_a4.get_frame_size() + \
                              0x10 # offset for s0

                # print(f"\nSelf modifying ROP address: {hex(backup_addr)}\n")

                #construct rop chain
                rop_chain += self.__charger.construct_frame(ra=self.__copy_a3.get_vaddr(), \
                                                            s0=backup_addr \
                                                            )

                rop_chain += self.__copy_a3.construct_frame(ra=self.__charger.get_vaddr())

                rop_chain += self.__charger.construct_frame(ra=self.__inc_a3.get_vaddr(), \
                                                            s1=-0x24, \
                                                            s4=self.__mov_a4_a3.get_vaddr() \
                                                            )
                
                rop_chain += self.__mov_a4_a3.construct_frame(ra=self.__mov_a0_a4.get_vaddr())

                rop_chain += self.__mov_a0_a4.construct_frame(ra=self.__charger.get_vaddr())

                rop_chain += self.__charger.construct_frame(ra=self.__load_s0.get_vaddr(), \
                                                            s1=self.__mov_a0_s0.get_vaddr(), \
                                                            s4=self.__inc_s0.get_vaddr(), \
                                                            s5=1, \
                                                            s7=self.__store_s0.get_vaddr(), \
                                                            s11=increment
                                                            )

                rop_chain += self.__mov_a0_s0.construct_frame(ra=self.__restore_a3.get_vaddr(), \
                                                              s0=backup_addr - 0x40, \
                                                              s3=1 \
                                                              )

                rop_chain += self.__restore_a3.construct_frame(ra=self.__and_a3_s0.get_vaddr(), \
                                                               s0= self.__addr_mask, \
                                                               s2=1 \
                                                               )
                
                rop_chain += self.__and_a3_s0.construct_frame(ra=self.__store_a0.get_vaddr(), \
                                                              s0=self.__addr_mask # will contain address written at runtime
                                                              ) 

                rop_chain += self.__store_a0.construct_frame(ra=next_gadget_addr)

                # advance sp
                new_sp += self.__get_instruction_len(instruction)

            elif instruction == '.' or instruction == ',':
                file_descriptor = 1 if instruction == '.' else 0
                syscall_no = 64 if instruction == '.' else 63

                backup_addr = new_sp + \
                              self.__charger.get_frame_size() + \
                              self.__copy_a3.get_frame_size() + \
                              0x58 # offset for s1

                # print(f"\nSelf modifying ROP address:   {hex(backup_addr)}")

                # construct rop chain
                rop_chain += self.__charger.construct_frame(ra=self.__copy_a3.get_vaddr(), \
                                                            s0=backup_addr, \
                                                            s4=self.__charger.get_vaddr(), \
                                                            s5=syscall_no, \
                                                            s7=self.__charger.get_vaddr()
                                                            )

                rop_chain += self.__copy_a3.construct_frame(ra=self.__init_a7.get_vaddr())    

                rop_chain += self.__charger.construct_frame(ra=self.__init_args.get_vaddr(), \
                                                            s2=1, \
                                                            s6=1, \
                                                            s7=self.__ecall.get_vaddr(), \
                                                            s10=file_descriptor, \
                                                            s1= self.__addr_mask # will contain address written at runtime
                                                            )

                rop_chain += self.__ecall.construct_frame(ra=self.__restore_a3.get_vaddr(), \
                                                          s0=backup_addr - 0x40 \
                                                          )
                                        
                rop_chain += self.__restore_a3.construct_frame(ra=self.__and_a3_s0.get_vaddr(), \
                                                               s0= self.__addr_mask 
                                                               )

                rop_chain += self.__and_a3_s0.construct_frame(ra=next_gadget_addr)

                # advance sp
                new_sp += self.__get_instruction_len(instruction)

        return new_sp, rop_chain

    def __match_brackets(self):
        brackets_stack = []

        for idx, instruction in enumerate(self.__bf_code):
            if instruction == '[':
                brackets_stack.append(idx)
            elif instruction == ']':
                if len(brackets_stack) == 0:
                    print("[Error] Invalid brainfuck code")
                    exit(0)
                
                self.__brackets[brackets_stack[-1]] = idx
                brackets_stack.pop()

        if len(brackets_stack) > 0:
            print("[Error] Invalid brainfuck code")
            exit(0)

    def __parse_jump(self, sp, zero_sp, nonzero_sp):
        backup_addr = sp + \
                      self.__pop_s0.get_frame_size() + \
                      self.__move_sp.get_frame_size() + \
                      self.__copy_a3.get_frame_size() + \
                      self.__mov_a4_a3.get_frame_size() + \
                      self.__mov_a0_a4.get_frame_size() + \
                      0x48 # offset for s3

        rop_chain = self.__pop_s0.construct_frame(ra=self.__move_sp.get_vaddr(),
                                                  s0=sp + self.__pop_s0.get_frame_size() + 0x50 \
                                                  )

        rop_chain += self.__move_sp.construct_frame(ra=self.__copy_a3.get_vaddr(), \
                                                    s0=backup_addr, \
                                                    s1=-0x24, \
                                                    s4=self.__mov_a4_a3.get_vaddr() \
                                                    )
        
        rop_chain += self.__copy_a3.construct_frame(ra=self.__inc_a3.get_vaddr())

        rop_chain += self.__mov_a4_a3.construct_frame(ra=self.__mov_a0_a4.get_vaddr())

        rop_chain += self.__mov_a0_a4.construct_frame(ra=self.__charger.get_vaddr())

        rop_chain += self.__charger.construct_frame(ra=self.__load_s0.get_vaddr(), \
                                                    s4=self.__mov_a0_s0.get_vaddr(), \
                                                    s3=self.__addr_mask # will contain address written at runtime
                                                    )

        rop_chain += self.__mov_a0_s0.construct_frame(ra=self.__charger.get_vaddr())

        rop_chain += self.__charger.construct_frame(ra=self.__beqz_a0.get_vaddr(), \
                                                    s0=zero_sp + 0x50 + self.__pop_s0.get_frame_size(), \
                                                    s2=1, \
                                                    s3=1, \
                                                    s7=self.__move_sp.get_vaddr() \
                                                    )

        rop_chain += self.__beqz_a0.construct_frame(ra=self.__add_a0_s0.get_vaddr(), \
                                                    a0=nonzero_sp - zero_sp \
                                                    )

        rop_chain += self.__add_a0_s0.construct_frame(ra=self.__mov_s0_a0.get_vaddr())

        return rop_chain

    def __parse_with_jumps(self, start_section, end_section, sp):
        if start_section >= end_section:
            return sp, b""

        for idx in range(start_section, end_section):
            if self.__bf_code[idx] == '[':
                sp1, chain1 = self.__parse_no_jumps(start_section, idx, sp)
                sp2, chain2 = self.__parse_with_jumps(idx + 1, self.__brackets[idx], sp1 + self.__get_instruction_len('['))
                sp3, chain3 = self.__parse_with_jumps(self.__brackets[idx] + 1, end_section, sp2 + self.__get_instruction_len(']'))

                open_bracket_sp = sp1 + self.__get_instruction_len('[')
                closed_bracket_sp = sp2 + self.__get_instruction_len(']')

                open_bracket_chain = self.__parse_jump(sp1, closed_bracket_sp, open_bracket_sp)
                closed_bracket_chain = self.__parse_jump(sp2, closed_bracket_sp, open_bracket_sp)

                return sp3, chain1 + open_bracket_chain + chain2 + closed_bracket_chain + chain3
        
        return self.__parse_no_jumps(start_section, end_section, sp)

    def jump_to_rop(self, rop_chain_start):
        return self.__charger.construct_frame(ra=self.__move_sp.get_vaddr(), \
                                              s0=rop_chain_start + 0x50 \
                                              )

    def parse(self, pointer_start, sp):
        # provide frame for the first jump to this address
        rop_chain = self.__move_sp.construct_frame(ra=self.__charger.get_vaddr())
        sp += self.__move_sp.get_frame_size()

        # initialize a3 to point to the middle of the tape
        rop_chain += self.__charger.construct_frame(ra=self.__init_a3.get_vaddr(), \
                                                    s4=self.__pop_s0.get_vaddr(), \
                                                    s7=pointer_start \
                                                    )
        sp += self.__charger.get_frame_size()
       
        # match brackets
        self.__match_brackets()

        # parse the actual instructions
        sp, chain = self.__parse_with_jumps(0, len(self.__bf_code), sp)       
        rop_chain += chain

        # end with an exit syscall and provide movesp frame to jump to it
        rop_chain += self.__pop_s0.construct_frame(ra=self.__move_sp.get_vaddr(),
                                                   s0=sp + self.__pop_s0.get_frame_size() + 0x50
                                                   )
        
        rop_chain += self.__move_sp.construct_frame(ra=self.__charger.get_vaddr())

        exit_syscall_no = 93
        rop_chain += self.__charger.construct_frame(ra=self.__init_a7.get_vaddr(), \
                                                    s2=1, \
                                                    s4=self.__init_args.get_vaddr(), \
                                                    s5=exit_syscall_no, \
                                                    s7=self.__ecall.get_vaddr() \
                                                    )

        return rop_chain