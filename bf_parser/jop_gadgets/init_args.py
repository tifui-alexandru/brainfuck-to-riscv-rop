from bf_parser.jop_gadgets_base_class import JOP_Gadget

class InitializeArgs(JOP_Gadget):
    '''
    mv a2, s6
    mv a1, s1
    mv a0, s10
    beqz s2, -0xcc
    jalr s7
    '''
    def __init__(self):
        super().__init__(0x1458c)