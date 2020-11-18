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

import os
from datetime import datetime


def create_logs_dir_if_not_exist():
    os.makedirs('logs', exist_ok=True)


def utc_datetime_string() -> str:
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
