from jop_gadgets import JOP_Gadget

class InitializeA3(JOP_Gadget):
    '''
    mv	a3, s7
    addi a2, sp, 0x40
    jalr s4
    '''
    def __init__(self):
        super().__init__(0x260f6)