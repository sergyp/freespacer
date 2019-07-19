
import click
from pathlib import Path

from freespacer.cleaning import clean


ENV_PREFIX = 'SPACER_'


@click.command()
@click.option('-s', '--need_space', type=str, required=True, envvar=f'{ENV_PREFIX}NEEDFREE')
@click.option('--no_delete', is_flag=True, default=False)
@click.option('--min_rest_count', type=int, default=0, envvar='{ENV_PREFIX}MIN_REST_COUNT')
@click.option('--max_del_count', type=int, default=-1, envvar='{ENV_PREFIX}MAX_DEL_COUNT')
@click.option('-m', '--mask', type=str, required=True, envvar='{ENV_PREFIX}MASK')
@click.argument('path', type=Path, required=True, envvar='{ENV_PREFIX}CLEANING_PATH')
def main(**kw):
    """
    need_space - required free space size in MiB
    path       - path to clean while not enought free space
    """
    clean(**kw)
