from bf_parser.jop_gadgets_base_class import JOP_Gadget

class InitA5(JOP_Gadget):
    '''
    mv a5, s6
    li a4, 0
    li a3, 0
    li a2, 0
    jalr s9
    '''
    def __init__(self):
        super().__init__(0x261d2)