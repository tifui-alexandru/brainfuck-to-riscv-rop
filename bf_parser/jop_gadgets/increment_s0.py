from bf_parser.jop_gadgets_base_class import JOP_Gadget

class IncrementS0(JOP_Gadget):
    '''
    add	s0, s0, s11
    li a7, 1
    li a6, 0
    mv a5, s5
    li a4, 0
    mv a3, s0
    mv a2, s4
    mv a1, s3
    mv a0, s2
    jalr s1
    '''
    def __init__(self):
        super().__init__(0x21756)