from gadgets import *

class BF_Parser():
    def __init__(self, bf_code):
        self.__bf_code = bf_code

        # get gadget objects
        self.__charger = Charger()
        self.__init_a3 = InitializeA3()
        self.__move_a3 = MoveA3()

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

        offset = [0] * 41
        data = [s11, s10, s9, s8, s7, s6, s5, s4, s3, s2, s1, s0, ra]
        self.__charger.set_stack_frame(offset + data)

    def parse(self):
        # initialize a3 to the middle of the tape
        initial_value = 0x41414141 # for debugging
        self.__construct_charger(ra=self.__init_a3.get_vaddr(), s4=self.__charger.get_vaddr(), s7=initial_value)

        rop_chain = self.__charger.print_vaddr() # charger address that overrides $ra
        rop_chain += self.__charger.print_gadget() # charger frame

        for instruction in self.__bf_code:
            if instruction == '>':
                self.__construct_charger(ra=self.__move_a3.get_vaddr(), s1=0x8, s4=self.__charger.get_vaddr())
                rop_chain += self.__charger.print_gadget()

            elif instruction == '<':
                self.__construct_charger(ra=self.__move_a3.get_vaddr(), s1=-0x8, s4=self.__charger.get_vaddr())
                rop_chain += self.__charger.print_gadget()

            elif instruction == '+':
                pass

            elif instruction == '-':
                pass

            elif instruction == '.':
                pass

            elif instruction == ',':
                pass

            elif instruction == '[':
                pass

            elif instruction == ']':
                pass

        return rop_chain