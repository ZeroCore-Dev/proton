import datetime
import struct
from typing import Any

WINDOWS_TICKS = int(1/10**-7)  # 10,000,000 (100 nanoseconds or .1 microseconds)
WINDOWS_EPOCH = datetime.datetime.strptime('1601-01-01 00:00:00',
                                           '%Y-%m-%d %H:%M:%S')
POSIX_EPOCH = datetime.datetime.strptime('1970-01-01 00:00:00',
                                         '%Y-%m-%d %H:%M:%S')
EPOCH_DIFF = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()  # 11644473600.0
WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF * WINDOWS_TICKS  # 116444736000000000.0

def get_time(filetime):
    """Convert windows filetime winticks to python datetime.datetime."""
    winticks = struct.unpack('<Q', filetime)[0]
    microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS
    return datetime.datetime.fromtimestamp(microsecs)

EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
EVERYTHING_REQUEST_EXTENSION = 0x00000008
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_CREATED = 0x00000020
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
EVERYTHING_REQUEST_DATE_ACCESSED = 0x00000080
EVERYTHING_REQUEST_ATTRIBUTES = 0x00000100
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME = 0x00000200
EVERYTHING_REQUEST_RUN_COUNT = 0x00000400
EVERYTHING_REQUEST_DATE_RUN = 0x00000800
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED = 0x00001000
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME = 0x00002000
EVERYTHING_REQUEST_HIGHLIGHTED_PATH = 0x00004000
EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME = 0x00008000

class flags:
    def __init__(self):
        self.need_file_name = 1
        self.need_full_path_and_file_name = 0
        self.need_path = 1
        self.need_extension = 0
        self.need_size = 1
        self.need_date_created = 0
        self.need_date_modified = 0
        self.need_date_accessed = 0
        self.need_attributes = 0
        self.need_file_list_file_name = 0
        self.need_run_count = 1
        self.need_date_run = 0
        self.need_date_recently_changed = 0
        self.need_highlighted_file_name = 0
        self.need_highlighted_full_path_and_file_name = 0
        self.modified = True
        self.val = self.value()

    def __setattr__(self, name: str, value: Any) -> None:
        if name != "val":
            self.__dict__["modified"] = True
        return super().__setattr__(name, value)

    def value(self):
        if not self.modified:
            return self.val

        value = 0
        value += self.need_file_name * EVERYTHING_REQUEST_FILE_NAME
        value += self.need_full_path_and_file_name * EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME
        value += self.need_path * EVERYTHING_REQUEST_PATH
        value += self.need_extension * EVERYTHING_REQUEST_EXTENSION
        value += self.need_size * EVERYTHING_REQUEST_SIZE
        value += self.need_date_created * EVERYTHING_REQUEST_DATE_CREATED
        value += self.need_date_modified * EVERYTHING_REQUEST_DATE_MODIFIED
        value += self.need_date_accessed * EVERYTHING_REQUEST_DATE_ACCESSED
        value += self.need_attributes * EVERYTHING_REQUEST_ATTRIBUTES
        value += self.need_file_list_file_name * EVERYTHING_REQUEST_FILE_LIST_FILE_NAME
        value += self.need_run_count * EVERYTHING_REQUEST_RUN_COUNT
        value += self.need_date_run * EVERYTHING_REQUEST_DATE_RUN
        value += self.need_date_recently_changed * EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED
        value += self.need_highlighted_file_name * EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME
        value += self.need_highlighted_full_path_and_file_name * EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME
        self.val = value
        self.modified = False
        return value