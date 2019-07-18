import re


UNITS = {
    "%": None,
    "B":  1,
    "KB": 10**3,
    "MB": 10**6,
    "GB": 10**9,
    "TB": 10**12,
    "PB": 10**15,
    "EB": 10**18,
    "ZB": 10**21,
    "YB": 10**24,
    "KiB": 2**10,
    "MiB": 2**20,
    "GiB": 2**30,
    "TiB": 2**40,
    "PiB": 2**50,
    "EiB": 2**60,
    "ZiB": 2**70,
    "YiB": 2**80,
}

_UNITS_UPPER = {k.upper(): v for k, v in UNITS.items()}


def to_bytes(s: str):
    if s.isdigit():
        return int(s), 'B'

    v = s.upper().replace(' ', '').replace(',', '.')
    if v.count('.') > 1:
        raise ValueError('Invalid value: {s!r}')

    r = '|'.join(_UNITS_UPPER.keys())
    m = re.match(f'^(.*?)({r})$', v)
    if not m:
        return int(v), 'B'

    v, unit = m.groups()
    k = _UNITS_UPPER[unit]
    v = float(v) if '.' in v else int(v)
    if unit == '%':
        return v, '%'

    v = int(v * k)
    return v, 'B'
