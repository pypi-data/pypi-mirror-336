import os
import ctypes


def vaset(path:str):

    current_path = os.path.dirname(os.path.abspath(__file__))

    dll_path = os.path.join(current_path, r'.\include\VnHardwareConf.dll')

    HdConfigLib = ctypes.CDLL(dll_path)

    HdConfigLib.vasetconf.argtypes = [ctypes.c_char_p]
    HdConfigLib.vasetconf.restype = ctypes.c_int

    return HdConfigLib.vasetconf(path.encode('utf-8'))

def xmlset(path:str, vn:str, index:str):

    current_path = os.path.dirname(os.path.abspath(__file__))

    dll_path = os.path.join(current_path, r'.\include\VnHardwareConf.dll')

    HdConfigLib = ctypes.CDLL(dll_path)

    HdConfigLib.xmlsetconf.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    HdConfigLib.xmlsetconf.restype = ctypes.c_int

    HdConfigLib.xmlsetconf.argtypes= [ctypes.c_char_p]

    return HdConfigLib.xmlsetconf(path.encode('utf-8'), vn.encode('utf-8'), index.encode('utf-8'))

