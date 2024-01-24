import sys
import psutil

# if sys.platform == 'win32':
#     for i in psutil.process_iter(["name"]):
#         if i.info["name"] == 'everything.exe' or i.info["name"] == 'Everything.exe':
#             print("Everything is running.", i.info["name"])
#         else:
#             raise ImportError('Everything is not running. Please run Everything first.')
# else:
#     raise NotImplementedError('This platform is not supported yet. Only Windows is supported currently.')

import ctypes
from .utils import *

#dll imports
try:
    everything_dll = ctypes.WinDLL ("dll/Everything64.dll")
except OSError:
    everything_dll = ctypes.WinDLL ("dll/Everything32.dll")

# basic setup
everything_dll.Everything_GetResultDateModified.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_ulonglong)]
everything_dll.Everything_GetResultSize.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_ulonglong)]
everything_dll.Everything_GetResultFileNameW.argtypes = [ctypes.c_int]
everything_dll.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p


# test for the service
everything_dll.Everything_SetSearchW("everything")
everything_dll.Everything_SetRequestFlags(EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH | EVERYTHING_REQUEST_SIZE | EVERYTHING_REQUEST_DATE_MODIFIED)

everything_dll.Everything_QueryW(1)
num_results = everything_dll.Everything_GetNumResults()

assert num_results > 0, "service malfunctioning. Maybe you should install everything service instread of everything lite"

# register buffer
_date_modified = ctypes.c_ulonglong(1)

class everything:

    def __init__(self):
        self.flags = flags()
        everything_dll.Everything_SetRequestFlags(self.flags.value())

    def setSearch(self, query):
        everything_dll.Everything_SetSearchW(query)
        everything_dll.Everything_QueryW(1)
        if self.flags.modified:
            everything_dll.Everything_SetRequestFlags(self.flags.value())
        return everything_dll.Everything_GetNumResults()
    
    def results(self):
        for i in range(num_results):
            tmp = {}    # hope this implementation won't cause memory leak
            tmp["file_name"] = everything_dll.Everything_GetResultFileNameW(i)

            if self.flags.need_date_modified:
                everything_dll.Everything_GetResultDateModified(i, _date_modified)
                tmp["date_modified"] = get_time(_date_modified)


            if self.flags.need_size:
                tmp["size"] = ctypes.c_ulonglong()
                everything_dll.Everything_GetResultSize(i,ctypes.byref(tmp["size"]))
            yield tmp

    def __getitem__(self, key):
        if key > num_results:
            raise IndexError("index out of range")
        retval = {}
        if self.flags.need_file_name:
            retval["file_name"] = everything_dll.Everything_GetResultFileNameW(key)
        if self.flags.need_date_modified:
            everything_dll.Everything_GetResultDateModified(key, _date_modified)
            retval["date_modified"] = get_time(_date_modified)
            
        if self.flags.need_size:
            retval["size"] = ctypes.c_ulonglong()
            everything_dll.Everything_GetResultSize(key,ctypes.byref(retval["size"]))
        
        return retval
