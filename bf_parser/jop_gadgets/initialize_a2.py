from bf_parser.jop_gadgets_base_class import JOP_Gadget

class InitializeA2(JOP_Gadget):
    '''
    mv a2, s6
    beqz s2, 0x1e
    jalr s7
    '''
    def __init__(self):
        super().__init__(0x144a6)