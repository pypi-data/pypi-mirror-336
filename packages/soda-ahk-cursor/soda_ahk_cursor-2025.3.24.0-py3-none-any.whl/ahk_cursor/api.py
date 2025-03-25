# https://gist.github.com/topin89/f8156a64ee79ff034cdf74c238b0dfa7


## Old info:
# Based on recipe http://code.activestate.com/recipes/576362-list-system-process-and-process-information-on-win/
# also hosted here https://github.com/ActiveState/code/blob/master/recipes/Python/576362_List_System_Process_Process/recipe-576362.py
# by winterTTr Dong , http://code.activestate.com/recipes/users/4164498/
# updated by topin89
# License: MIT

from ctypes import (
    c_long,
    c_int,
    c_void_p,
    c_size_t,
    c_ulong,
    c_wchar,
)
from ctypes import windll
from ctypes import Structure
from ctypes import sizeof, POINTER, pointer

# const variable
TH32CS_SNAPPROCESS = 2
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPTHREAD = 0x00000004

STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF

MAX_PATH = 260
MAX_MODULE_NAME32 = 255


# c_wchar instead of c_char is the only difference
class PROCESSENTRY32W(Structure):
    _fields_ = [
        ("dwSize", c_ulong),
        ("cntUsage", c_ulong),
        ("th32ProcessID", c_ulong),
        ("th32DefaultHeapID", c_size_t),
        ("th32ModuleID", c_ulong),
        ("cntThreads", c_ulong),
        ("th32ParentProcessID", c_ulong),
        ("pcPriClassBase", c_long),
        ("dwFlags", c_ulong),
        ("szExeFile", c_wchar * MAX_PATH),
    ]


# foreign functions

## CreateToolhelp32Snapshot
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.reltype = c_long
CreateToolhelp32Snapshot.argtypes = [c_ulong, c_ulong]


## Process32FirstW
Process32FirstW = windll.kernel32.Process32FirstW
Process32FirstW.argtypes = [c_void_p, POINTER(PROCESSENTRY32W)]
Process32FirstW.rettype = c_int

## Process32NextW
Process32NextW = windll.kernel32.Process32NextW
Process32NextW.argtypes = [c_void_p, POINTER(PROCESSENTRY32W)]
Process32NextW.rettype = c_int


CloseHandle = windll.kernel32.CloseHandle


# see also: https://docs.rs/tasklist/latest/src/tasklist/lib.rs.html#77
def GetProcessByName(name: str):
    hProcessSnap = c_void_p(0)
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

    pe32 = PROCESSENTRY32W()
    pe32.dwSize = sizeof(PROCESSENTRY32W)
    ret = Process32FirstW(hProcessSnap, pointer(pe32))
    found = False
    while ret:
        pass
        x = pe32.szExeFile

        if x == name:
            found = True
            break

        ret = Process32NextW(hProcessSnap, pointer(pe32))

    CloseHandle(hProcessSnap)
    return found
