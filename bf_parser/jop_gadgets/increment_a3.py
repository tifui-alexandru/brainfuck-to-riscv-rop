from bf_parser.jop_gadgets_base_class import JOP_Gadget

class IncrementA3(JOP_Gadget):
    '''
    add	a3, a3, s1
    addi a2, sp, 0x48
    mv a0, s5
    jalr s4
    '''
    def __init__(self):
        super().__init__(0x2af60)