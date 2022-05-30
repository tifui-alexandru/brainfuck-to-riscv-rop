from bf_parser.jop_gadgets_base_class import JOP_Gadget

class StoreS0(JOP_Gadget):
    '''
    fsd	fs0, 0x28(a3)
    bnez a1, 0xae
    lw s9, 0x18(sp)
    jalr tp, 0x6d6(s8)
    '''
    def __init__(self):
        super().__init__(0x69446)