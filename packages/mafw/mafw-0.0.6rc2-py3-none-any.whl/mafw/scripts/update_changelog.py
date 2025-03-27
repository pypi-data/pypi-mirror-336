"""
Module provides a simplified script to perform MAFw changelog update using ``auto-changelog``.
It can be used as pre-commit entry point and also in CI.

The basic idea is that this command is invoking the auto-changelog tool to generate a temporary changelog. The
checksum of such a temporary changelog is then compared with the actual one and if it is different, then the current
one is replaced with the newly created.

When committing the changelog update please use mute as commit type, to avoid having a new changelog generated
containing the changelog update commit.

"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click
from rich import print

from mafw.__about__ import __version__ as mafw_version
from mafw.tools.file_tools import file_checksum


@click.command()
@click.option(
    '-i',
    '--input-file',
    default=Path.cwd() / Path('CHANGELOG.md'),
    type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, allow_dash=False),
    help='The path to the input changelog file. Default CHANGELOG.md',
)
@click.option('-f', '--force-recreate', is_flag=True, default=False, help='Force recreation of CHANGELOG.md')
def update(input_file: click.Path | Path | str, force_recreate: bool) -> int:
    """Execute the auto-changelog program with default configuration for MAFw.

    \f

    :return: 0: if the changelog was successfully updated.
        1: if the changelog was already up to date.
        -1: if an error occurred during the process.
    """
    exe = 'auto-changelog'
    if shutil.which(exe) is None:
        print(
            f'[red]{exe} is not available in this environment. Are you sure, you have installed MAFw with optional dev?'
        )
        return -1

    description = 'MAFw: Modular Analysis Framework'
    latest_version = f'v{mafw_version}'
    tag_prefix = 'v'

    if isinstance(input_file, (click.Path, str)):
        input_file = Path(str(input_file))

    if not input_file.exists():
        print(f'[orange3]No input file {input_file.name} found. Creating a new one.')
        input_file.touch()

    if force_recreate:
        print(f'[orange3]{input_file.name} will be recreated.')
        input_file.unlink()
        input_file.touch()

    original_changelog_cs = file_checksum(input_file)

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        file = Path(tmp_dir_name) / Path(input_file.name)
        args = [
            exe,
            '-o',
            str(file),
            '-d',
            f'"{description}"',
            '--gitlab',
            '-v',
            latest_version,
            '--tag-prefix',
            tag_prefix,
        ]
        subprocess.run(args)
        new_changelog_cs = file_checksum(file)

        if new_changelog_cs != original_changelog_cs:
            shutil.copy(file, input_file)
            print(f'[green]{input_file.name} successfully updated')
            return 0
        else:
            print(f'[cyan]{input_file.name} was already up to date')
            return 2


def main() -> None:
    """Script entry point"""
    ret_val = update(standalone_mode=False)
    sys.exit(ret_val)


if __name__ == '__main__':
    main()
