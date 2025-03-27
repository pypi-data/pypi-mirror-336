import os
import stat
from os import linesep, remove
from pathlib import Path
from sys import platform
from tempfile import gettempdir
from unittest.mock import call, patch

from pytest import mark

from moht import utils


def test_parse_cleaning_success():
    err = ''
    out = f'{linesep}CLEANING: "FLG - Balmora\'s Underworld V1.1.esp" ...{linesep}' \
          f'Loaded cached Master: <DATADIR>/morrowind.esm{linesep}' \
          f'Loaded cached Master: <DATADIR>/tribunal.esm{linesep}' \
          f'Loaded cached Master: <DATADIR>/bloodmoon.esm{linesep}' \
          f' Cleaned duplicate record (STAT): in_dwrv_corr3_02{linesep}' \
          f' Cleaned redundant AMBI,WHGT from CELL: omaren ancestral tomb{linesep}' \
          f'Output saved in: "1/FLG - Balmora\'s Underworld V1.1.esp"{linesep}' \
          f'Original unaltered: "FLG - Balmora\'s Underworld V1.1.esp"{linesep}{linesep}' \
          f'Cleaning Stats for "FLG - Balmora\'s Underworld V1.1.esp":{linesep}' \
          f'                duplicate record:     1{linesep}' \
          f'             redundant CELL.AMBI:     1{linesep}' \
          f'             redundant CELL.WHGT:     1{linesep}'
    assert utils.parse_cleaning(out, err, "FLG - Balmora's Underworld V1.1.esp") == (True, 'saved')


def test_parse_cleaning_not_modified():
    err = ''
    out = """CLEANING: "FLG - Balmora's Underworld V1.1.esp" ...
Loaded cached Master: <DATADIR>/morrowind.esm
Loaded cached Master: <DATADIR>/tribunal.esm
Loaded cached Master: <DATADIR>/bloodmoon.esm
FLG - Balmora's Underworld V1.1.esp was not modified"""
    assert utils.parse_cleaning(out, err, "FLG - Balmora's Underworld V1.1.esp") == (False, 'not modified')


def test_parse_cleaning_no_1_master():
    err = """Use of uninitialized value in -s at /home/emc/git/Modding-OpenMW/modhelpertool/src/moht/resources/tes3cmd-0.37w line 6282.
Use of uninitialized value $curr_size in numeric eq (==) at /home/emc/git/Modding-OpenMW/modhelpertool/src/moht/resources/tes3cmd-0.37w line 6283.
Use of uninitialized value $curr_size in concatenation (.) or string at /home/emc/git/Modding-OpenMW/modhelpertool/src/moht/resources/tes3cmd-0.37w line 6287.
Cache Invalidated for: oaab_data.esm (curr_size == , prev_size == 1269934) at /home/emc/git/Modding-OpenMW/modhelpertool/src/moht/resources/tes3cmd-0.37w line 6287.

[ERROR (Caldera.esp): Master: oaab_data.esm not found in <DATADIR>]"""
    out = """CLEANING: "Caldera.esp" ...
Loaded cached Master: <DATADIR>/morrowind.esm
Loaded cached Master: <DATADIR>/tribunal.esm
Loaded cached Master: <DATADIR>/bloodmoon.esm
Loading Master: oaab_data.esm
Caldera.esp was not modified"""
    assert utils.parse_cleaning(out, err, 'Caldera.esp') == (False, 'oaab_data.esm not found')


def test_parse_cleaning_no_2_master():
    err = """[ERROR (Library of Vivec Overhaul - Full.esp): Master: tamriel_data.esm not found in <DATADIR>]
[ERROR (Library of Vivec Overhaul - Full.esp): Master: oaab_data.esm not found in <DATADIR>]"""
    out = """CLEANING: "Library of Vivec Overhaul - Full.esp" ...
Loading Master: morrowind.esm
Loading Master: tribunal.esm
Loading Master: bloodmoon.esm
Loading Master: tamriel_data.esm
Loading Master: oaab_data.esm
 Cleaned duplicate object instance (in_velothismall_ndoor_01 FRMR: 482716) from CELL: vivec, hall of wisdom
 Cleaned redundant AMBI,WHGT from CELL: vivec, hall of wisdom
 Cleaned redundant AMBI,WHGT from CELL: vivec, library of vivec
Output saved in: "1/Library of Vivec Overhaul - Full.esp"
Original unaltered: "Library of Vivec Overhaul - Full.esp"
Cleaning Stats for "Library of Vivec Overhaul - Full.esp":
       duplicate object instance:     1
             redundant CELL.AMBI:     2
             redundant CELL.WHGT:     2"""
    assert utils.parse_cleaning(out, err, 'Library of Vivec Overhaul - Full.esp') == (False, 'tamriel_data.esm not found**oaab_data.esm not found')


def test_parse_cleaning_check_bin_no_config_inifiles():
    err = """Can't locate Config/IniFiles.pm in @INC (you may need to install the Config::IniFiles module) (@INC contains: /usr/lib/perl5/5.36/site_perl /usr/share/perl5/site_perl /usr/lib/perl5/5.36/vendor_perl /usr/share/perl5/vendor_perl /usr/lib/perl5/5.36/core_perl /usr/share/perl5/core_perl) at /home/emc/git/Modding-OpenMW/modhelpertool/src/moht/resources/tes3cmd-0.37w line 107.
BEGIN failed--compilation aborted at /home/emc/git/Modding-OpenMW/modhelpertool/src/moht/resources/tes3cmd-0.37w line 107."""
    out = ''
    assert utils.parse_cleaning(out, err, 'Caldera.esp') == (False, 'Config::IniFiles module')


def test_parse_cleaning_check_bin_ok():
    err = """WARNING: Can't find "Data Files" directory, functionality reduced. You should first cd (change directory) to somewhere under where Morrowind is installed.
Usage: tes3cmd COMMAND OPTIONS plugin...
VERSION: 0.37w
tes3cmd is a low-level command line tool that can examine, edit, and delete
records from a TES3 plugin for Morrowind. It can also generate various patches
and clean plugins too.
COMMANDS
  active
    Add/Remove/List Plugins in your load order.
  clean
    Clean plugins of Evil GMSTs, junk cells, and more.
  common
    Find record IDs common between two plugins."""
    out = ''
    assert utils.parse_cleaning(out, err, 'Caldera.esp') == (True, 'Usage')


def test_run_cmd():
    tes3cmd = 'tes3cmd-0.37v.exe' if platform == 'win32' else 'tes3cmd-0.37w'
    plugin = 'some_plugin.esp'
    cmd = f"{Path(__file__).resolve().parent / '..' / 'src' / 'moht' / 'resources' / tes3cmd} clean {plugin}"
    out, err = utils.run_cmd(cmd)
    cleaning, reason = utils.parse_cleaning(out, err, plugin)
    assert cleaning is False
    if reason == 'Not tes3cmd':
        assert out == f'{linesep}CLEANING: "{plugin}" ...{linesep}'
        assert f'FATAL ERROR ({plugin}): Invalid input file (No such file or directory)' in err
    else:
        assert reason == 'Config::IniFiles module'


@mark.parametrize('local_ver, out_err, result', [
    ('0.37.0', ("""Collecting tox==3.25.1
  Using cached tox-3.25.1-py2.py3-none-any.whl (85 kB)
Collecting wheel==0.37.1
  Using cached wheel-0.37.1-py2.py3-none-any.whl (35 kB)
Requirement already satisfied: pluggy>=0.12.0 in /home/emc/.pyenv/versions/3.10.5/envs/moth310/lib/python3.10/site-packages (from tox==3.25.1) (1.0.0)
Would install tox-3.25.1 wheel-0.37.1""", ''), (False, 'Update available: 0.37.1')),
    ('0.37.1', ('Requirement already satisfied: wheel==0.37.1 in /home/emc/.pyenv/versions/3.10.5/envs/moth310/lib/python3.10/site-packages (0.37.1)', ''), (True, 'No updates')),
])
def test_is_latest_ver_success(local_ver, out_err, result):
    with patch.object(utils, 'run_cmd') as run_cmd_mock:
        run_cmd_mock.return_value = out_err
        assert utils.is_latest_ver('wheel', current_ver=local_ver) == result
        run_cmd_mock.assert_called_once_with('pip install --dry-run --no-color --timeout 3 --retries 1 --progress-bar off --upgrade wheel')


@mark.parametrize('local_ver, effect, result', [
    ('0.37.1', [('', """Usage:
  pip install [options] <requirement specifier> [package-index-options] ...
  pip install [options] -r <requirements file> [package-index-options] ...
  pip install [options] [-e] <vcs project url> ...
  pip install [options] [-e] <local project path> ...
  pip install [options] <archive url/path> ...

no such option: --dry-run
"""), ('', '')], (True, 'Version check failed, unknown switch: --dry-run')),
    ('0.37.1', [('', """Usage:
  pip install [options] <requirement specifier> [package-index-options] ...
  pip install [options] -r <requirements file> [package-index-options] ...
  pip install [options] [-e] <vcs project url> ...
  pip install [options] [-e] <local project path> ...
  pip install [options] <archive url/path> ...

no such option: --dry-run
"""), ("""Package      Version
------------ -------
packaging    21.3
pip          22.2
wheel        0.37.1
platformdirs 2.5.2
pluggy       1.0.0
""", '')], (True, 'Version check failed, old pip: 22.2')),
])
def test_is_latest_ver_check_failed(local_ver, effect, result):
    with patch.object(utils, 'run_cmd', side_effect=effect) as run_cmd_mock:
        assert utils.is_latest_ver('wheel', current_ver=local_ver) == result
        run_cmd_mock.assert_has_calls([call('pip install --dry-run --no-color --timeout 3 --retries 1 --progress-bar off --upgrade wheel'),
                                       call('pip list')])


def test_get_all_plugins():
    return_val = ('/home', ('user',), ('user2',)), ('/home/user', (), ('plugin1.esp', 'plugin2.esm')),
    with patch.object(utils, 'walk', return_value=return_val):
        assert utils.get_all_plugins(mods_dir='/home') == [Path('/home/user/plugin1.esp'), Path('/home/user/plugin2.esm')]


def test_get_required_esm():
    plugins = [Path('/home/user/OAAB - Foyada Mamaea.ESP'), Path("/home/user/Building Up Uvirith's Legacy1.1.ESP")]
    with patch.object(utils, 'run_cmd') as run_cmd_mock:
        run_cmd_mock.side_effect = [('Morrowind.esm\nTribunal.esm\n', ''),
                                    ('Morrowind.esm\nTribunal.esm\nBloodmoon.esm\nOAAB_Data.esm\n', '')]
        assert utils.get_required_esm(plugins=plugins, omwcwd='omwcwd') == {'Morrowind.esm', 'Tribunal.esm', 'Bloodmoon.esm', 'OAAB_Data.esm'}


def test_get_required_esm_not_on_plugin_list():
    plugins = [Path('/home/user/Aldruhn/Ald-ruhn.esp')]
    with patch.object(utils, 'run_cmd') as run_cmd_mock:
        run_cmd_mock.return_value = '', ''
        assert utils.get_required_esm(plugins=plugins, omwcwd='omwcwd') == set()


@mark.skipif(condition=platform != 'linux', reason='Run only on Linux')
@mark.parametrize('dir_path', ['/home/user/mods', Path('/home/user/mods')], ids=['string', 'path like object'])
def test_rm_dirs_with_subdirs_linux(dir_path):
    with patch.object(utils, 'rmtree') as rmtree_mock:
        utils.rm_dirs_with_subdirs(dir_path, ['plugin1', 'plugin2'])
        rmtree_mock.assert_has_calls([call(Path('/home/user/mods/plugin1'), ignore_errors=True),
                                      call(Path('/home/user/mods/plugin2'), ignore_errors=True)])


@mark.skipif(condition=platform != 'win32', reason='Run only on Windows')
@mark.parametrize('dir_path', ['C:\\Users\\mplic\\mods', Path('C:\\Users\\mplic\\mods')], ids=['string', 'path like object'])
def test_rm_dirs_with_subdirs_windows(dir_path):
    with patch.object(utils, 'rmtree') as rmtree_mock:
        utils.rm_dirs_with_subdirs(dir_path, ['plugin1', 'plugin2'])
        rmtree_mock.assert_has_calls([call(Path('C:\\Users\\mplic\\mods\\plugin1'), ignore_errors=True),
                                      call(Path('C:\\Users\\mplic\\mods\\plugin2'), ignore_errors=True)])


def test_find_missing_esm():
    side_effect = [
        [
            ('/home', ('user1', 'user2'), ()),
            ('/home/user1', ('mods', 'datafiles'), ()),
            ('/home/user1/datafiles', ('plugin3',), ('plugin3.esm', 'plugin4.esm', 'plugin4.esm'))
        ],
        [
            ('/home', ('user1', 'user2'), ()),
            ('/home/user1', ('mods', 'datafiles'), ()),
            ('/home/user1/mods', (), ('plugin1.esm', 'plugin2.esm', 'plugin3.esp', 'plugin5.esm'))]
    ]
    with patch.object(utils, 'walk', side_effect=side_effect):
        result = utils.find_missing_esm(dir_path='/home/user1/mods',
                                        data_files='/home/user1/datafiles',
                                        esm_files={'plugin1.esm', 'plugin2.esm', 'plugin3.esm', 'plugin4.esm'})
        assert result == [Path('/home/user1/mods/plugin1.esm'),
                          Path('/home/user1/mods/plugin2.esm')]


@mark.skipif(condition=platform != 'linux', reason='Run only on Linux')
def test_copy_filelist_linux():
    from pathlib import PosixPath
    with patch.object(utils, 'copy2') as copy2_mock:
        utils.copy_filelist(file_list=[Path('/home/user/mods/plugin1.esm'), Path('/home/user/mods/plugin2.esm')], dest_dir=Path('/home/user/datafiles'))
        copy2_mock.assert_has_calls([call(PosixPath('/home/user/mods/plugin1.esm'), PosixPath('/home/user/datafiles')),
                                     call(PosixPath('/home/user/mods/plugin2.esm'), PosixPath('/home/user/datafiles'))])


@mark.skipif(condition=platform != 'win32', reason='Run only on Windows')
def test_copy_filelist_windows():
    from pathlib import WindowsPath
    with patch.object(utils, 'copy2') as copy2_mock:
        utils.copy_filelist(file_list=[Path('C:\\Users\\mplic\\datafiles\\plugin1.esm'), Path('C:\\Users\\mplic\\datafiles\\plugin2.esm')], dest_dir=Path('C:\\Users\\mplic\\datafiles'))
        copy2_mock.assert_has_calls([call(WindowsPath('C:/Users/mplic/datafiles/plugin1.esm'), WindowsPath('C:/Users/mplic/datafiles')),
                                     call(WindowsPath('C:/Users/mplic/datafiles/plugin2.esm'), WindowsPath('C:/Users/mplic/datafiles'))])


@mark.skipif(condition=platform != 'linux', reason='Run only on Linux')
def test_rm_copied_extra_ems_linux():
    from pathlib import PosixPath
    with patch.object(utils, 'remove') as remove_mock:
        utils.rm_copied_extra_esm(esm=[Path('/home/user/mods/plugin1.esm'), Path('/home/user/mods/plugin2.esm')], data_files=Path('/home/user/datafiles'))
        remove_mock.assert_has_calls([call(PosixPath('/home/user/datafiles/plugin1.esm')), call(PosixPath('/home/user/datafiles/plugin2.esm'))])


@mark.skipif(condition=platform != 'win32', reason='Run only on Windows')
def test_rm_copied_extra_ems_windows():
    from pathlib import WindowsPath
    with patch.object(utils, 'remove') as remove_mock:
        utils.rm_copied_extra_esm(esm=[Path('C:\\Users\\mplic\\mods\\plugin1.esm'), Path('C:\\Users\\mplic\\mods\\plugin2.esm')], data_files=Path('C:\\Users\\mplic\\datafiles'))
        remove_mock.assert_has_calls([call(WindowsPath('C:/Users/mplic/datafiles/plugin1.esm')), call(WindowsPath('C:/Users/mplic/datafiles/plugin2.esm'))])


def test_rm_copied_extra_esm_exception_handling():
    with patch.object(utils, 'remove', side_effect=FileNotFoundError):
        utils.rm_copied_extra_esm(esm=[Path('/home/user/mods/plugin1.esm'), Path('/home/user/mods/plugin2.esm')], data_files=Path('/home/user/datafiles'))


@mark.parametrize('args, result', [
    ((9.50, '%M:%S'), '00:09'),
    ((9.50, '%S'), '09'),
    ((19.24, '%M:%S'), '00:19'),
    ((19.24, '%S'), '19'),
    ((58.1, '%M:%S'), '00:58'),
    ((128.95, '%M:%S'), '02:08'),
    ((453.83, '%M:%S'), '07:33'),
    ((453.83, '%H:%M:%S'), '00:07:33'),
])
def test_get_string_duration(args, result):
    assert utils.get_string_duration(*args) == result


def test_read_write_yaml_cfg_file():
    test_tmp_yaml = Path(gettempdir()) / 'c.yaml'
    cfg = {'setting_1': {'setting_2': 2}}
    utils.write_config(cfg, test_tmp_yaml)
    d_cfg = utils.read_config(test_tmp_yaml)
    assert d_cfg == cfg
    with open(test_tmp_yaml, 'w+') as f:
        f.write(',')
    d_cfg = utils.read_config(test_tmp_yaml)
    assert len(d_cfg) == 0
    remove(test_tmp_yaml)


@mark.skipif(condition=platform != 'win32', reason='Run only on Windows')
def test_set_path_hidden_windows():
    hidden_file = Path(gettempdir()) / '.hidden.file'
    with open(hidden_file, 'w+') as f:
        f.write(',')
    assert not bool(os.stat(hidden_file).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    assert utils.set_path_hidden(hidden_file)
    assert bool(os.stat(hidden_file).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    remove(hidden_file)
