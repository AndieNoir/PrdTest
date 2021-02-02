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

import math
import os

from prdtest.data.generators.base import Generator


class ComscireF33E62D4(Generator, id='comscire_f33e62d4'):

    _GET_BOOL_BITS_PER_TRIAL = 5

    if os.name == 'nt':
        import win32com.client
        _qng = win32com.client.Dispatch('QWQNG.QNG')
    else:
        import ctypes
        import platform
        _qwqng_wrapper = ctypes.cdll.LoadLibrary('./libqwqng-wrapper-x86-64.so' if platform.machine().endswith('64') else './libqwqng-wrapper.so')
        _qwqng_wrapper.GetQwqngInstance.restype = ctypes.c_void_p
        _qwqng_wrapper.RandBytes.argtypes = [ctypes.c_void_p, ctypes.c_int]
        _qwqng_wrapper.RandBytes.restype = ctypes.POINTER(ctypes.c_char)
        _qwqng_wrapper.RandUniform.argtypes = [ctypes.c_void_p]
        _qwqng_wrapper.RandUniform.restype = ctypes.c_double
        _qwqng_wrapper.Clear.argtypes = [ctypes.c_void_p]
        _qng_pointer = _qwqng_wrapper.GetQwqngInstance()

    def get_bool(self) -> bool:
        # R.M. Brier et al., "Psi Application: Part II. The Majority Vote Technique—Analysis and Observations", Journal
        # of Parapsychology, vol. 34, pp. 26-36, 1970.
        bits = []
        data = self._get_bytes(math.ceil(ComscireF33E62D4._GET_BOOL_BITS_PER_TRIAL / 8))
        for i in range(len(data)):
            for j in range(8):
                bits.append(1 if data[i] >> j & 1 == 1 else 0)
        bits = bits[:ComscireF33E62D4._GET_BOOL_BITS_PER_TRIAL]
        return bits.count(1) > ComscireF33E62D4._GET_BOOL_BITS_PER_TRIAL / 2

    def get_int_between_0_and_4(self) -> int:
        if os.name == 'nt':
            self._qng.Clear()
            return int(self._qng.RandUniform * 5)
        else:
            self._qwqng_wrapper.Clear(self._qng_pointer)
            return int(self._qwqng_wrapper.RandUniform(self._qng_pointer) * 5)

    def _get_bytes(self, length: int) -> bytes:
        if os.name == 'nt':
            return self._get_bytes_windows(length)
        else:
            return self._get_bytes_linux(length)

    def _get_bytes_windows(self, length: int) -> bytes:
        self._qng.Clear()
        if length <= 8192:
            return bytes(self._qng.RandBytes(length))
        else:
            data = bytearray()
            for _ in range(length // 8192):
                data.extend(bytearray(self._qng.RandBytes(8192)))
            bytes_needed = length % 8192
            if bytes_needed != 0:
                data.extend(bytearray(self._qng.RandBytes(bytes_needed)))
            return bytes(data)

    def _get_bytes_linux(self, length: int) -> bytes:
        self._qwqng_wrapper.Clear(self._qng_pointer)
        if length <= 8192:
            return self._qwqng_wrapper.RandBytes(self._qng_pointer, length)[:length]
        else:
            data = bytearray()
            for _ in range(length // 8192):
                data.extend(self._qwqng_wrapper.RandBytes(self._qng_pointer, 8192)[:8192])
            bytes_needed = length % 8192
            if bytes_needed != 0:
                data.extend(self._qwqng_wrapper.RandBytes(self._qng_pointer, bytes_needed)[:bytes_needed])
            return bytes(data)
