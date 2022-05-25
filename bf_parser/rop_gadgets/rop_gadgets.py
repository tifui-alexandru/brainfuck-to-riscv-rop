import struct

class ROP_Gadget():
    def __init__(self, vaddr, frame_size):
        self.__vaddr = vaddr
        self.__stack_frame = None
        self.__frame_size = frame_size

    def get_vaddr(self):
        return self.__vaddr

    def get_frame_size(self):
        return self.__frame_size

    def __set_stack_frame(self, stack_frame):
        self.__stack_frame = stack_frame

    def print_gadget(self):
        ans = b""

        if self.__stack_frame is None:
            print("[Error] no stack frame given for charger")
        else:
            for value in self.__stack_frame:
                ans += struct.pack("q", value)

        return ans