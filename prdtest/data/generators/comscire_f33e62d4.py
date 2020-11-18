# Copyright (C) 2020 AndieNoir
#
# PrdTest is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PrdTest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PrdTest.  If not, see <https://www.gnu.org/licenses/>.

import ctypes
import math
import platform

from prdtest.data.generators.base import Generator


class ComscireF33E62D4(Generator, id='comscire_f33e62d4'):

    _GET_BOOL_BITS_PER_TRIAL = 199

    def __init__(self):
        self._qwqng_wrapper = ctypes.cdll.LoadLibrary('./libqwqng-wrapper-x86-64.so' if platform.machine().endswith('64') else './libqwqng-wrapper.so')
        self._qwqng_wrapper.GetQwqngInstance.restype = ctypes.c_void_p
        self._qwqng_wrapper.RandBytes.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self._qwqng_wrapper.RandBytes.restype = ctypes.POINTER(ctypes.c_char)
        self._qwqng_wrapper.RandUniform.argtypes = [ctypes.c_void_p]
        self._qwqng_wrapper.RandUniform.restype = ctypes.c_double
        self._qwqng_wrapper.Clear.argtypes = [ctypes.c_void_p]
        self._qng_pointer = self._qwqng_wrapper.GetQwqngInstance()

    def get_bool(self) -> tuple:
        raw_bits = []
        data = self._get_bytes(math.ceil(ComscireF33E62D4._GET_BOOL_BITS_PER_TRIAL / 8))
        for i in range(len(data)):
            for j in range(8):
                raw_bits.append(1 if data[i] >> j & 1 == 1 else 0)
        raw_bits = raw_bits[:ComscireF33E62D4._GET_BOOL_BITS_PER_TRIAL]
        return raw_bits.count(1) > ComscireF33E62D4._GET_BOOL_BITS_PER_TRIAL / 2, raw_bits

    def get_int_between_0_and_4(self) -> int:
        self._qwqng_wrapper.Clear(self._qng_pointer)
        return int(self._qwqng_wrapper.RandUniform(self._qng_pointer) * 5)

    def _get_bytes(self, length: int) -> bytes:
        self._qwqng_wrapper.Clear(self._qng_pointer)
        if length <= 8192:
            return self._qwqng_wrapper.RandBytes(self._qng_pointer, length)[:length]
        else:
            data = bytearray()
            for i in range(length // 8192):
                data.extend(self._qwqng_wrapper.RandBytes(self._qng_pointer, 8192)[:8192])
            bytes_needed = length % 8192
            if bytes_needed != 0:
                data.extend(self._qwqng_wrapper.RandBytes(self._qng_pointer, bytes_needed)[:bytes_needed])
            return bytes(data)
