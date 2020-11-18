PrdTest
=======

A Python web app to compare RNGs' responsiveness to mind influence.

Running
-------

1. Run the following commands

   ```
   pip3 install -r requirements.txt
   python3 -m prdtest
   ```

2. Open http://localhost:57011

Adding a new random number generator
------------------------------------

1.  Create a class that extends `Generator` and override the `get_bool` method

    Example:

    ```python
    # prdtest/generator/dev_hwrng.py
    
    from prdtest.generator.base import Generator
    
    
    class DevHwrng(Generator, id='my_rng'):

        def __init__(self):
            self._hwrng = open('/dev/hwrng', 'rb')

        def get_bool(self):
            return self._hwrng.read(1)[0] & 1 == 1

        def get_int_between_0_and_4(self) -> int:
            return self._hwrng.read(1)[0] % 5
    ```

2.  Set the generator class on `config.py`

    ```python
    # prdtest/config.py
    
    from prdtest.generator.dev_hwrng import DevHwrng
    
    
    GENERATOR_CLASSES = [
        # ...,
        DevHwrng,
    ]
    ```

License
-------

    Copyright (C) 2020 AndieNoir
    
    PrdTest is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PrdTest is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    
    You should have received a copy of the GNU Affero General Public License
    along with PrdTest.  If not, see <https://www.gnu.org/licenses/>.
