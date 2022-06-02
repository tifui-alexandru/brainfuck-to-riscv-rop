from bf_parser.rop_gadgets_base_class import ROP_Gadget

class Beqz_a0(ROP_Gadget):
    '''
    beqz a0, 0x4bee2
    ld a0, 0x18(sp)
    ld ra, 0x28(sp)
    addi sp, sp, 0x30
    jr ra
   
    0x4bee2
    ld ra, 0x28(sp)
    addi sp, sp, 0x30
    jr ra
    '''

    def __init__(self):
        super().__init__(0x4bd94, 1264)

    def construct_frame(self, a0, ra):
        data = [0, 0, 0, a0, 0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()