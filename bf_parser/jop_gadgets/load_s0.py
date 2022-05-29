from bf_parser.jop_gadgets_base_class import JOP_Gadget

class LoadS0(JOP_Gadget):
    '''
    fld	fs0, 0x60(a3)
    addi a5, sp, 0x8
    li a4, 0
    li a7, 0
    li a6, 0
    mv a3, s3
    addi a2, sp, 0x10
    addi a1, s0, 0x50
    mv a0, s5
    jalr s4
    '''
    def __init__(self):
        super().__init__(0x16ee6)