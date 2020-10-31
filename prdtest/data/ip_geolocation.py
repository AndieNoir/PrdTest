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

import ipaddress

import requests

_cache = {}


def get_country_alpha2(ip_address: str):
    if ipaddress.ip_address(ip_address).is_private:
        return None
    elif ip_address not in _cache:
        try:
            _cache[ip_address] = requests.get(f'https://api.ipgeolocationapi.com/geolocate/{ip_address}').json()['alpha2'].upper()
        except:
            return None
    return _cache[ip_address]
