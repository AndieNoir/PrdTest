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


class Generator:
    def __init_subclass__(cls, id: str, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.id = id

    def get_bool(self) -> bool:
        pass

    def get_int_between_0_and_4(self) -> int:
        pass
