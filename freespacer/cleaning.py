
import click
import shutil
from pathlib import Path
from collections import Counter

from .data_volume_parser import to_bytes


def is_space_enough(need, path=Path('.')):
    total, used, free = shutil.disk_usage(str(path))
    need_space_value, unit = to_bytes(need)
    if unit == '%':
        need_space_value = int(total * need_space_value / 100)

    return free >= need_space_value


def clean(need_space, no_delete, min_rest_count, max_del_count, mask, path):
    """
    need_space - required free space size in MiB
    path       - path to clean while not enought free space
    """

    files = list(sorted(path.glob(mask)))
    deleted = []
    stat = Counter(
        realy_deleted_count=0,
        errors_count=0,
        deletion_tries_count=0,
        deletion_pretend_count=0,
        skipped_count=0,
    )

    while (
        len(files) > min_rest_count
        and (max_del_count < 0 or len(deleted) < max_del_count)
        and not is_space_enough(need_space, path=path)
    ):
        f = files.pop(0)
        deleted.append(f)
        stat['deletion_pretend_count'] += 1

        if no_delete:
            click.echo('SKIPPED {f}'.format(**locals()))
            stat['skipped_count'] += 1
        else:
            stat['deletion_tries_count'] += 1
            try:
                f.unlink()
            except Exception as e:
                stat['errors_count'] += 1
                click.echo('ERROR   {f}  # {e}'.format(**locals()))
            else:
                stat['realy_deleted_count'] += 1
                click.echo('DELETED {f}'.format(**locals()))

    if not(len(files) > min_rest_count):
        l = len(files)
        click.echo('Done by min_rest_count={min_rest_count} => {l}'.format(**locals()), err=True)

    if not(max_del_count < 0 or len(deleted) < max_del_count):
        l = len(deleted)
        click.echo('Done by max_del_count={max_del_count} > {l}'.format(**locals()), err=True)

    if is_space_enough(need_space, path=path):
        total, used, free = shutil.disk_usage(str(path))
        click.echo('Done by space, there is enough: {total} from {free} is >= {need_space}'.format(**locals()), err=True)

    max_stat_key = max(map(len, stat.keys()))
    max_stat_value = max(map(len, map(str, stat.values())))
    for k, v in stat.items():
        click.echo('{k:{max_stat_key}}: {v:{max_stat_value}}'.format(**locals()), err=True)
