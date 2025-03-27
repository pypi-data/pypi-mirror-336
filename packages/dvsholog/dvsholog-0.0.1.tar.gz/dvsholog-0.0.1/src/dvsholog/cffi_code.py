#Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
#Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
"""
    Copyright National Research Foundation (SARAO), 2005-2025. All Rights Reserved.
    Author: Mattieu de Villiers (email: mattieu@sarao.ac.za)
"""

import os
import importlib
from cffi import FFI

ffi = FFI()

PATH = os.path.dirname(__file__)

with open(os.path.join(PATH, "c_code.h")) as f:
    ffi.cdef(f.read(), override=True)

fnm=os.path.join(PATH, 'c_code'+importlib.machinery.EXTENSION_SUFFIXES[0])
lib=ffi.dlopen(fnm) # lib=ffi.dlopen('/home/mattieu/py3env/lib/python3.8/site-packages/dvsholog/c_code.cpython-38-x86_64-linux-gnu.so')

