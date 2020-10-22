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
