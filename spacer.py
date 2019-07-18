
import click
import shutil
from pathlib import Path
from collections import Counter
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

UNITS_UPPER = {k.upper(): v for k, v in UNITS.items()}


def to_bytes(s: str):
    if s.isdigit():
        return int(s), 'B'

    v = s.upper().replace(' ', '').replace(',', '.')
    if v.count('.') > 1:
        raise ValueError('Invalid value: {s!r}')

    r = '|'.join(UNITS_UPPER.keys())
    m = re.match(f'^(.*?)({r})$', v)
    if not m:
        return int(v), 'B'

    v, unit = m.groups()
    k = UNITS_UPPER[unit]
    v = float(v) if '.' in v else int(v)
    if unit == '%':
        return v, '%'

    v = int(v * k)
    return v, 'B'


def is_space_enough(need, path=Path('.')):
    total, used, free = shutil.disk_usage(str(path))
    need_space_value, unit = to_bytes(need)
    if unit == '%':
        need_space_value = int(total * need_space_value / 100)

    return free >= need_space_value


ENV_PREFIX = 'SPACER_'


@click.command()
@click.option('-s', '--need_space', type=str, required=True, envvar=f'{ENV_PREFIX}NEEDFREE')
@click.option('--no_delete', is_flag=True, default=False)
@click.option('--min_rest_count', type=int, default=0, envvar='{ENV_PREFIX}MIN_REST_COUNT')
@click.option('--max_del_count', type=int, default=-1, envvar='{ENV_PREFIX}MAX_DEL_COUNT')
@click.option('-m', '--mask', type=str, default='*', envvar='{ENV_PREFIX}MASK')
@click.argument('path', type=Path, required=False, default=Path('.'), envvar='{ENV_PREFIX}CLEANING_PATH')
def main(need_space: str, no_delete: bool, min_rest_count: int, max_del_count: int, mask: str, path: Path):
    """
    need_space - required free space size in MiB
    path       - path to clean while not enought free space
    """

    files = list(sorted(path.glob(mask)))
    deleted = []
    stat = Counter(realy_deleted_count=0, errors_count=0, deletion_tries_count=0, deletion_pretend_count=0)
    while (
        len(files) > min_rest_count
        and (max_del_count < 0 or len(deleted) < max_del_count)
        and not is_space_enough(need_space, path=path)
    ):
        f = files.pop(0)
        deleted.append(f)
        click.echo(f'RM {f}')
        stat['deletion_pretend_count'] += 1

        if not no_delete:
            stat['deletion_tries_count'] += 1
            try:
                f.unlink()
            except Exception as e:
                click.echo(f"ERROR while delete {f}: {e}")
                stat['errors_count'] += 1
            else:
                stat['realy_deleted_count'] += 1

    if not(len(files) > min_rest_count):
        click.echo(f'Done by min_rest_count={min_rest_count} => {len(files)}', err=True)

    if not((max_del_count < 0 or len(deleted) < max_del_count)):
        click.echo(f'Done by max_del_count={max_del_count} > {len(deleted)}', err=True)

    if is_space_enough(need_space, path=path):
        total, used, free = shutil.disk_usage(str(path))
        click.echo(f'Done by space, there is enough: {total} from {free} is >= {need_space}', err=True)

    max_stat_key = max(map(len, stat.keys()))
    max_stat_value = max(map(len, map(str, stat.values())))
    for k, v in stat.items():
        click.echo(f'{k:{max_stat_key}}: {v:{max_stat_value}}', err=True)

if __name__ == '__main__':
    main()