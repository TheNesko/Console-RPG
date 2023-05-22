from imports import *

class Key:
    KEY_tab = 9
    KEY_enter = 13
    KEY_ESC = 27
    KEY_space = 32
    KEY_plus = 43
    KEY_minus = 45
    KEY_0 = 48
    KEY_1 = 49
    KEY_2 = 50
    KEY_3 = 51
    KEY_4 = 52
    KEY_5 = 53
    KEY_6 = 54
    KEY_7 = 55
    KEY_8 = 56
    KEY_9 = 57
    KEY_EQUAL = 61
    KEY_FLOOR = 95
    KEY_a = 97
    KEY_d = 100
    KEY_e = 101
    KEY_n = 110
    KEY_q = 113
    KEY_s = 115
    KEY_w = 119
    KEY_y = 121
    KEY_del = 4301
    KEY_Aup = 4401
    KEY_Adown = 4402
    KEY_Aright = 4403
    KEY_Aleft = 4404

    @staticmethod
    def get_input():
        ky = msvcrt.getch()
        if ky in [b'\x00', b'\xe0']:
            ky = msvcrt.getch()
            if ky == b'S':
                return Key.KEY_del
            if ky == b'H':
                return Key.KEY_Aup
            if ky == b'P':
                return Key.KEY_Adown
            if ky == b'M':
                return Key.KEY_Aright
            if ky == b'K':
                return Key.KEY_Aleft
        return ord(ky.lower())
