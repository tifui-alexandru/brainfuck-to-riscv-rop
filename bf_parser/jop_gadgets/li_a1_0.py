from jop_gadgets import JOP_Gadget

class LiA1_0(JOP_Gadget):
    '''
    li a1, 0
    jalr s1
    '''
    def __init__(self):
        super().__init__(0x21848)