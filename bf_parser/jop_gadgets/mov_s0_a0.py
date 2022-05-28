from bf_parser.jop_gadgets_base_class import JOP_Gadget

class MovS0_A0(JOP_Gadget):
    '''
    mv s0, a0
    add	s10, s10, s4
    beqz s3, -0x38
    mv a2, s6
    mv a1, s1
    mv a0, s10
    beqz s2, -0xcc
    jalr s7
    '''
    def __init__(self):
        super().__init__(0x14504)