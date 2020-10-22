# Copyright (C) 2020 AndieNoir
#
# PrdTest is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PrdTest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PrdTest.  If not, see <https://www.gnu.org/licenses/>.

from prdtest.data.generators.comscire_f33e62d4 import ComscireF33E62D4
from prdtest.data.generators.pseudorandom_2797e9c1 import Pseudorandom2797E9C1


GENERATOR_CLASSES = [
    ComscireF33E62D4,
    Pseudorandom2797E9C1,
]