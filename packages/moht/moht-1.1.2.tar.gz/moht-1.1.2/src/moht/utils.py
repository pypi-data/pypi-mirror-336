from datetime import date, datetime, time, timedelta
from logging import getLogger
from os import linesep, remove, walk
from pathlib import Path
from pprint import pformat
from re import MULTILINE, findall, search
from shlex import split
from shutil import copy2, rmtree
from subprocess import PIPE, Popen
from sys import platform

from packaging import version
from yaml import FullLoader, YAMLError, load, safe_dump

logger = getLogger(__name__)


def run_cmd(cmd: str) -> tuple[str, str]:
    """
    Run command and return stdout and stderr.

    :param cmd: command to execute
    :return: stdout, stderr
    """
    cmd2exec = split(cmd) if platform == 'linux' else cmd
    logger.debug(f'CMD: {cmd2exec}')
    stdout, stderr = Popen(cmd2exec, stdout=PIPE, stderr=PIPE).communicate()
    out, err = stdout.decode('utf-8'), stderr.decode('utf-8')
    logger.debug(f'StdOut: {out}')
    logger.debug(f'StdErr: {err}')
    return out, err


def parse_cleaning(out: str, err: str, mod_filename: str) -> tuple[bool, str]:
    """
    Parse output of cleaning command printout.

    :param out: Command STANDARD OUTPUT
    :param err: Command STANDARD ERROR
    :param mod_filename: Mod filename
    :return: Result and reason
    """
    result = False, 'Not tes3cmd'
    ceases = [
        {'args': (fr'\[ERROR \({mod_filename}\): Master: (.* not found) in <DATADIR>]', err, MULTILINE),
         'result': False},
        {'args': (fr'{mod_filename} was (not modified)', out, MULTILINE),
         'result': False},
        {'args': (fr'Output (saved) in: "1/{mod_filename}"{linesep}Original unaltered: "{mod_filename}"', out, MULTILINE),
         'result': True},
        {'args': (r'Can\'t locate Config/IniFiles.pm in @INC \(you may need to install the (Config::IniFiles module)\)', err, MULTILINE),
         'result': False},
        {'args': (r'(Usage): tes3cmd COMMAND OPTIONS plugin...', err, MULTILINE),
         'result': True},
    ]
    for data in ceases:
        match = findall(*data['args'])  # type: ignore
        if match:
            result = bool(data['result']), '**'.join(match)
            break
    return result


def is_latest_ver(package: str, current_ver: str) -> tuple[bool, str]:
    """
    Check if installed package is the latest.

    :param package: package name
    :param current_ver: currently installed version
    """
    remote_ver = current_ver
    extra_data = 'No updates'
    problem = False
    out, err = run_cmd(f'pip install --dry-run --no-color --timeout 3 --retries 1 --progress-bar off --upgrade {package}')
    match = search(fr'Would install\s.*{package}-([\d.-]+)', out)
    if match:
        remote_ver = match.group(1)
        logger.debug(f'Latest available version: {remote_ver}')
        extra_data = f'Update available: {remote_ver}'
    match = search(r'no such option:\s(.*)', err)
    if match:
        problem = True
        extra_data = f'Version check failed, unknown switch: {match.group(1)}'
        logger.warning(extra_data)
        out, _ = run_cmd('pip list')
        match = search(r'pip\s*([\d.]*)', out)
        if match:
            pip_ver = match.group(1)
            extra_data = f'Version check failed, old pip: {pip_ver}'
            logger.debug(f'Pip version: {pip_ver}')
    latest = _compare_versions(package, current_ver, remote_ver)
    if latest and current_ver == remote_ver and not problem:
        extra_data = 'No updates'
    return latest, extra_data


def _compare_versions(package: str, current_ver: str, remote_ver: str) -> bool:
    """
    Compare versions.

    :param package:
    :param current_ver:
    :param remote_ver:
    :return:
    """
    latest = False
    if version.parse(remote_ver) > version.parse(current_ver):
        logger.info(f'There is new version of {package}: {remote_ver}')
    elif version.parse(remote_ver) <= version.parse(current_ver):
        logger.info(f'{package} is up-to-date version: {current_ver}')
        latest = True
    return latest


def get_all_plugins(mods_dir: Path) -> list[Path]:
    """
    Get list of absolute paths  for all plugins in mods_dir directory.

    :param mods_dir: rood directory of mods
    :return: List of Path objects
    """
    return [Path(root) / filename
            for root, _, files in walk(mods_dir)
            for filename in files
            if filename.lower().endswith('.esp') or filename.lower().endswith('.esm')]


def get_required_esm(plugins: list[Path], omwcwd: Path) -> set[str]:
    """
    Get set of required esm files.

    :param plugins:
    :param omwcwd:
    :return:
    """
    output = set()
    for plugin in plugins:
        out, _ = run_cmd(f'{omwcwd} masters "{plugin}"')
        output.update(out.split('\n'))
    output.remove('')
    return output


def rm_dirs_with_subdirs(dir_path: str | Path, subdirs: list[str]) -> None:
    """
    Remove directories with specific subdirectories.

    :param dir_path: root directory, string or path like object
    :param subdirs: list of subdirectories of root to remove
    """
    for directory in [Path(dir_path) / subdir for subdir in subdirs]:
        logger.debug(f'Remove: {directory}')
        rmtree(directory, ignore_errors=True)


def find_missing_esm(dir_path: Path, data_files: Path, esm_files: set[str]) -> list[Path]:
    """
    Find missing esm files in Morrowind Data Files folder.

    :param dir_path: directory path of mods
    :param data_files: Morrowind Data Files directory
    :param esm_files: set of esm file names
    :return: list of files
    """
    in_datafiles = {filename
                    for _, _, files in walk(data_files)
                    for filename in files
                    if filename in esm_files}
    logger.debug(f'esm found in Data Files: {in_datafiles}')
    missing_files = esm_files - in_datafiles
    logger.debug(f'Missing esm files: {missing_files}')
    file_list = [Path(root) / filename
                 for root, _, files in walk(dir_path)
                 for filename in files
                 if filename in missing_files]
    debug_file_list = f'\n{pformat(file_list)}' if len(file_list) > 0 else file_list
    logger.debug(f'Missing esm found in Mods: {debug_file_list}')
    return file_list


def copy_filelist(file_list: list[Path], dest_dir: Path) -> None:
    """
    Copy files from file_list to dest_dir.

    :param file_list: list of files to copy
    :param dest_dir: destination directory
    """
    for file_path in file_list:
        logger.debug(f'Copy: {file_path} -> {dest_dir}')
        copy2(file_path, dest_dir)


def rm_copied_extra_esm(esm: list[Path], data_files: Path) -> None:
    """
    Remove extra esm files from Morrowind Data Files folder.

    :param esm: list of esm files
    :param data_files: Morrowind Data Files directory
    """
    for esm_file in esm:
        esm_path = data_files / esm_file.name
        try:
            remove(esm_path)
        except FileNotFoundError:
            logger.debug(f'File not found: {esm_path}')
        else:
            logger.debug(f'Remove: {esm_path}')


def get_string_duration(seconds: float, time_format='%M:%S') -> str:
    """
    Return time duration as string with formatting.

    :param seconds: number of seconds as float
    :param time_format: way of formatting output i.e. '%M:%S'
    :return: time as string with format
    """
    now = datetime.combine(date.today(), time()) + timedelta(seconds=seconds)
    return now.strftime(time_format)


def read_config(yaml_file: Path | str) -> dict[str, dict[str, str | int | bool]]:
    """
    Read configuration from yaml file and return dict.

    :raise OSError: when yaml_file do not exist or is not a file
    :param yaml_file: absolute path to configuration yaml
    :return: configuration as dict
    """
    try:
        with open(yaml_file) as ymlfile:
            data = load(ymlfile, Loader=FullLoader)
    except (YAMLError, TypeError):
        data = {}
    return data


def write_config(data: dict[str, dict[str, str | int | bool]], yaml_file: Path | str, mode='w') -> None:
    """
    Write python dict as yaml file.

    :raise OSError: when yaml_file do not exist or is not a file
    :param data: dict of configuration
    :param yaml_file: absolute path to configuration yaml
    :param mode: writing mode
    """
    with open(yaml_file, mode) as ymlfile:
        safe_dump(data, ymlfile, default_flow_style=False)


def set_path_hidden(full_path: Path | str) -> bool:
    """
    Set path as hidden.

    On Linux/Mac always True, real change only on Windows.
    :param full_path: path as string or Path-like object
    :return: operation result
    """
    ret = True
    if platform == 'win32':
        from ctypes import windll  # type: ignore
        ret = windll.kernel32.SetFileAttributesW(str(full_path), 0x02)
    return bool(ret)
