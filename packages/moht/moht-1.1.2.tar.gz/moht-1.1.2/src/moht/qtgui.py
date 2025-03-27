import traceback
import webbrowser
from argparse import Namespace
from collections.abc import Callable
from functools import partial
from logging import getLogger
from os import chdir, makedirs, remove
from pathlib import Path
from pprint import pformat
from shutil import copy2, move
from sys import exc_info, platform, version_info
from tempfile import gettempdir
from time import time

import qtawesome
from PySide6 import __version__ as pyside6_ver
from PySide6.QtCore import QCoreApplication, QFile, QIODevice, QMetaObject, QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtCore import __version__ as qt6_ver
from PySide6.QtGui import QAction, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFileDialog, QLabel, QLineEdit, QMainWindow, QMenu, QMessageBox, QProgressBar, QPushButton,
                               QRadioButton, QStackedWidget, QStatusBar, QSystemTrayIcon, QTreeWidget, QTreeWidgetItem, QWidget)

from moht import OMWCMD, TES3CMD, VERSION, qtgui_rc, utils
from moht.utils import read_config, set_path_hidden, write_config

_ = qtgui_rc  # prevent to remove import statement accidentally
REP_COL_PLUGIN = 0
REP_COL_STATUS = 1
REP_COL_TIME = 2


def tr(text: str, context='@default') -> str:
    """
    Translate wrapper function.

    :param text: string to translate
    :param context: for translation
    :return:
    """
    return QCoreApplication.translate(context=context, sourceText=text)


class MohtQtGui(QMainWindow):
    """Moht PySide6 GUI."""
    def __init__(self, cli_args: Namespace) -> None:
        """
        Mod Helper Tool PySide6 GUI.

        :param cli_args: Parameters from CLI
        """
        super().__init__()
        UiLoader().loadUi(':/ui/ui/qtgui.ui', self)
        self._find_children()
        self.logger = getLogger(__name__)
        self.threadpool = QThreadPool.globalInstance()
        self.logger.debug(f'QThreadPool with {self.threadpool.maxThreadCount()} thread(s)')
        self.tes3cmd_le_status = {'le_mods_dir': False, 'le_morrowind_dir': False, 'le_tes3cmd': False}
        self.systray = QSystemTrayIcon()
        self.traymenu = QMenu()
        self.auto_save = False
        self.progress = 0
        self.no_of_plugins = 0
        self.missing_esm: list[Path] = []
        self.duration = 0.0
        self.conf_file = ''
        self.config = {}
        self.last_dir: dict[str, str] = {d: '' for d in ['le_mods_dir', 'le_morrowind_dir', 'le_tes3cmd', 'cfg_dir', 'le_masters_plugin']}
        self._init_tray()
        self._init_menu_bar()
        self._init_tes3cmd_clean()
        self._init_omwcmd_masters()
        self.omwcmd = MohtQtGui._set_executable_path(OMWCMD[platform])
        self._apply_gui_configuration(self._get_yaml_file(cli_args.yamlfile))
        # need read configuration first
        self._init_test3cmd_buttons()
        self._init_tree_report()
        self.statusbar.showMessage(self.tr('ver. {0}').format(VERSION))
        self._set_icons()

    def _get_yaml_file(self, cli_yaml_file: str) -> str:
        """
        Select best yaml configuration.

        * First try yaml form CLI, then
        * use default form package and in the end
        * try load form user home directory

        :param cli_yaml_file:
        :return:
        """
        yaml_file = Path(__file__).resolve().with_name('default.yaml')
        user_moht_dir = Path.home() / '.moht'
        user_moht_yaml = user_moht_dir / 'moht.yaml'
        if cli_yaml_file:
            yaml_file = cli_yaml_file
            self.conf_file = cli_yaml_file
        elif not user_moht_yaml.is_file():
            makedirs(name=user_moht_dir, exist_ok=True)
            copy2(yaml_file, user_moht_yaml)
            set_path_hidden(user_moht_dir)
            self.conf_file = user_moht_yaml
            yaml_file = user_moht_yaml
        elif user_moht_yaml.is_file():
            self.conf_file = user_moht_yaml
            yaml_file = user_moht_yaml
        return yaml_file

    def _init_tray(self) -> None:
        """Initialize of system tray icon."""
        self.systray.setIcon(QIcon(':/images/img/moht.ico'))
        self.systray.setVisible(True)
        self.systray.setToolTip(f'Moht {VERSION}')
        self.traymenu.addAction(self.actionCheckUpdates)
        self.traymenu.addAction(self.actionQuit)
        self.systray.setContextMenu(self.traymenu)
        self.systray.activated.connect(self.activated)

    def _init_menu_bar(self) -> None:
        """Initialize of menubar."""
        self.actionLoad.triggered.connect(self.load_config)
        self.actionSave.triggered.connect(self.save_config)
        self.actionSave_as.triggered.connect(self.save_config_as)
        self.actionQuit.triggered.connect(self.close)
        self.actionAboutMoht.triggered.connect(AboutDialog(self).open)
        self.actionAboutQt.triggered.connect(partial(self._show_message_box, kind_of='aboutQt', title='About Qt'))
        self.actionReportIssue.triggered.connect(self._report_issue)
        self.actionCheckUpdates.triggered.connect(self.check_updates)

    # <=><=><=><=><=><=><=><=><=><=><=> tes3cmd init clean <=><=><=><=><=><=><=><=><=><=><=>
    def _init_tes3cmd_clean(self) -> None:
        """Initialize events for tes3clean."""
        self.le_mods_dir.textChanged.connect(partial(self._is_dir_exists, widget_name='le_mods_dir'))
        self.le_morrowind_dir.textChanged.connect(partial(self._is_dir_exists, widget_name='le_morrowind_dir'))
        self.le_tes3cmd.textChanged.connect(partial(self._is_file_exists, widget_name='le_tes3cmd'))
        self.le_mods_dir.textChanged.connect(self.trigger_autosave)
        self.le_morrowind_dir.textChanged.connect(self.trigger_autosave)
        self.le_tes3cmd.textChanged.connect(self.trigger_autosave)

        self.rb_custom.toggled.connect(self._rb_custom_toggled)
        for ver in [37, 40]:
            getattr(self, f'rb_{ver}').toggled.connect(partial(self._rb_tes3cmd_toggled, ver))

        self.cb_auto_save.toggled.connect(self.autosave_toggled)
        self.cb_rm_backup.toggled.connect(self.trigger_autosave)
        self.cb_rm_cache.toggled.connect(self.trigger_autosave)

    def _init_test3cmd_buttons(self) -> None:
        """Initialize events for buttons of tes3clean."""
        self.pb_mods_dir.clicked.connect(partial(self._run_file_dialog, for_load=True, for_dir=True,
                                                 last_dir=lambda: self.last_dir['le_mods_dir'], widget_name='le_mods_dir'))
        self.pb_morrowind_dir.clicked.connect(partial(self._run_file_dialog, for_load=True, for_dir=True,
                                                      last_dir=lambda: self.last_dir['le_morrowind_dir'], widget_name='le_morrowind_dir'))
        self.pb_tes3cmd.clicked.connect(partial(self._run_file_dialog, for_load=True, for_dir=False,
                                                last_dir=lambda: self.last_dir['le_tes3cmd'], widget_name='le_tes3cmd'))
        self.pb_report.clicked.connect(partial(self.stacked_clean.setCurrentIndex, 1))
        self.pb_clean.clicked.connect(self._pb_clean_clicked)

    def _rb_tes3cmd_toggled(self, version: int, state: bool) -> None:
        """
        Toggle between version of tes3cmd.

        :param version: shortcut fo version as integer
        :param state: of radio button
        """
        if state:
            self.tes3cmd = MohtQtGui._set_executable_path(TES3CMD[platform][version])
        self.trigger_autosave()

    def _rb_custom_toggled(self, state: bool) -> None:
        """
        Enable and disable custom version of tes3cmd.

        :param state: of radio button
        """
        self.le_tes3cmd.setEnabled(state)
        self.pb_tes3cmd.setEnabled(state)
        self.trigger_autosave()

    def autosave_toggled(self) -> None:
        """Toggle action for autosave checkbox."""
        if self.cb_auto_save.isChecked():
            self.save_config()
        else:
            self.conf_file = ''
            self.statusbar.clearMessage()

    def _is_dir_exists(self, text: str, widget_name: str) -> None:
        """
        Check if directory exists.

        :param text: contents of text field
        :param widget_name: widget name
        """
        dir_exists = Path(text).is_dir()
        self.logger.debug(f'Path: {text} for {widget_name} exists: {dir_exists}')
        self._line_edit_handling_and_last_directory(widget_name, dir_exists, text)

    def _is_file_exists(self, text: str, widget_name) -> None:
        """
        Check if file exists.

        :param text: contents of text field
        :param widget_name: widget name
        """
        file_exists = Path(text).is_file()
        self.logger.debug(f'Path: {text} for {widget_name} exists: {file_exists}')
        self._line_edit_handling_and_last_directory(widget_name, file_exists, text)

    def _line_edit_handling_and_last_directory(self, widget_name: str, path_exists: bool, path_name: str) -> None:
        """
        Mark text of LineEdit as red if path does not exist.

        Save last visited path (starting directory for QFileWidget) base of path_name.

        :param widget_name: widget name
        :param path_exists: bool for path existence
        :param path_name: full path name
        """
        self.tes3cmd_le_status[widget_name] = path_exists
        if path_exists and widget_name == 'tes3cmd':
            getattr(self, widget_name).setStyleSheet('')
            self.last_dir[widget_name] = str(Path(path_name).resolve().parent)
            result = self._check_clean_bin()
            if not result:
                self.tes3cmd_le_status[widget_name] = result
                getattr(self, widget_name).setStyleSheet('color: red;')
        elif path_exists and widget_name != 'tes3cmd':
            getattr(self, widget_name).setStyleSheet('')
            self.last_dir[widget_name] = str(Path(path_name).resolve().parent)
        else:
            getattr(self, widget_name).setStyleSheet('color: red;')
        self._handle_clean_button()

    def _check_clean_bin(self) -> bool:
        """
        Verify if binary file is correct.

        :return: True if file is correct
        """
        self.logger.debug('Checking tes3cmd')
        try:
            out, err = utils.run_cmd(f'{self.tes3cmd} help')
            result, reason = utils.parse_cleaning(out, err, '')
        except OSError as exp:
            self.logger.debug('Checking selected tes3cmd file', exc_info=True)
            result = False
            reason = str(exp)
        self.logger.debug(f'Result: {result}, Reason: {reason}')
        if not result:
            self.statusbar.showMessage(self.tr('Error: {0}').format(reason))
            if 'Config::IniFiles' in reason:
                msg = self.tr('''
Check for `perl-Config-IniFiles` or a similar package.
Use you package manage:

Arch / Manjaro (AUR):
yay -S perl-config-inifiles

Gentoo:
emerge dev-perl/Config-IniFiles

Debian / Ubuntu / Mint:
apt install libconfig-inifiles-perl

OpenSUSE:
zypper install perl-Config-IniFiles

Fedora / CentOS / RHEL:
dnf install perl-Config-IniFiles.noarch''')
            elif 'Not tes3cmd' in reason:
                msg = self.tr('Selected file is not a valid tes3cmd executable.\n\nPlease select a correct binary file.')
            else:
                msg = reason
            self._show_message_box(kind_of='warning', title='Not tes3cmd', message=msg)
        return result

    def _handle_clean_button(self) -> None:
        """Enable /disable Clean button base on status of LineEdits."""
        if all(self.tes3cmd_le_status.values()):
            self.pb_clean.setEnabled(True)
        else:
            self.pb_clean.setEnabled(False)

    # <=><=><=><=><=><=><=><=><=><=><=> tes3cmd clean <=><=><=><=><=><=><=><=><=><=><=>
    def _pb_clean_clicked(self) -> None:
        """Event for Clean button clicked."""
        self.progressbar.setValue(0)
        self.progress = 0
        self._clear_tree_report()
        self.pb_report.setEnabled(True)
        self._set_icons(button='pb_clean', icon_name='fa5s.spinner', color='green', spin=True)
        self.pb_clean.clicked.disconnect()
        all_plugins = utils.get_all_plugins(mods_dir=self.mods_dir)
        self.logger.debug(f'all_plugins: {len(all_plugins)}:\n{pformat(all_plugins)}')
        self.no_of_plugins = len(all_plugins)
        self.logger.debug(f'to_clean: {self.no_of_plugins}:\n{pformat(all_plugins)}')
        self.statusbar.showMessage(self.tr('Plugins to clean: {0} - See Report').format(self.no_of_plugins))
        req_esm = utils.get_required_esm(plugins=all_plugins, omwcwd=self.omwcmd)
        self.logger.debug(f'Required esm: {req_esm}')
        self.missing_esm = utils.find_missing_esm(dir_path=self.mods_dir, data_files=self.morrowind_dir, esm_files=req_esm)
        utils.copy_filelist(self.missing_esm, self.morrowind_dir)
        self.duration = time()
        self.progressbar.setValue(int(100 / (self.no_of_plugins * 2)))
        for idx, plug in enumerate(all_plugins, 1):
            self.logger.debug(f'Start: {idx} / {self.no_of_plugins}')
            self.run_in_background(job=partial(self._clean_start, plug=plug),
                                   signal_handlers={'error': self._error_during_clean,
                                                    'result': self._clean_finished})

    def _clean_start(self, plug: Path) -> tuple[Path, bool, str, float, str, str]:
        """
        Run cleaning command.

        :param plug: path to plugin
        :return: details of cleaning result
        """
        start = time()
        chdir(self.morrowind_dir)
        self.logger.debug(f'Copy: {plug} -> {self.morrowind_dir}')
        copy2(plug, self.morrowind_dir)
        mod_file = plug.name
        out, err = utils.run_cmd(f'{self.tes3cmd} clean --output-dir --overwrite "{mod_file}"')
        result, reason = utils.parse_cleaning(out, err, mod_file)
        self.logger.debug(f'Result: {result}, Reason: {reason}')
        if result:
            clean_plugin = self.morrowind_dir / '1' / mod_file
            self.logger.debug(f'Move: {clean_plugin} -> {plug}')
            move(clean_plugin, plug)
        if self.cb_rm_backup.isChecked():
            mod_path = self.morrowind_dir / mod_file
            self.logger.debug(f'Remove: {mod_path}')
            remove(mod_path)
        self.logger.debug(f'Done: {mod_file}')
        duration = time() - start
        return plug, result, reason, duration, out, err

    def _error_during_clean(self, exc_tuple: tuple[Exception, str, str]) -> None:
        """
        Error during cleaning process.

        :param exc_tuple: exception details.
        """
        exc_type, exc_val, exc_tb = exc_tuple
        self.logger.warning(f'{exc_type.__class__.__name__}: {exc_val}')
        self.logger.debug(exc_tb)

    def _clean_finished(self, clean_result: tuple[Path, bool, str, float, str, str]) -> None:
        """
        Finish cleaning process.

        :param clean_result: details of cleaning result
        """
        self._add_report_data(*clean_result)
        self.progress += 1
        percent = self.progress * 100 / self.no_of_plugins
        self.logger.debug(f'Progress: {percent:.2f} %')
        self.progressbar.setValue(int(percent))
        if self.progress == self.no_of_plugins:
            self._clean_done()

    def _clean_done(self) -> None:
        """Clean process is done."""
        self.progressbar.setValue(100)
        if self.cb_rm_cache.isChecked():
            cachedir = 'tes3cmd' if platform == 'win32' else '.tes3cmd-3'
            utils.rm_dirs_with_subdirs(dir_path=self.morrowind_dir, subdirs=['1', cachedir])
        utils.rm_copied_extra_esm(self.missing_esm, self.morrowind_dir)
        cleaning_time = time() - self.duration
        self.logger.debug(f'Total time: {cleaning_time} s')
        self._set_icons(button='pb_clean', icon_name='fa5s.hand-sparkles', color='brown')
        if cleaning_time <= 60.0:
            duration = f'{utils.get_string_duration(seconds=cleaning_time, time_format="%S")} [sec]'
        else:
            duration = f'{utils.get_string_duration(seconds=cleaning_time, time_format="%M:%S")} [min:sec]'
        self.statusbar.showMessage(self.tr('Done. Took: {0}').format(duration))
        self.pb_clean.clicked.connect(self._pb_clean_clicked)

    # <=><=><=><=><=><=><=><=><=><=><=> tes3cmd report <=><=><=><=><=><=><=><=><=><=><=>
    def _init_tree_report(self):
        """Initialize tree structure of report."""
        self.tree_report.setColumnWidth(REP_COL_PLUGIN, 320)
        self.tree_report.setColumnWidth(REP_COL_STATUS, 130)
        self.tree_report.setColumnWidth(REP_COL_TIME, 60)
        self.tree_report.itemDoubleClicked.connect(self._item_double_clicked)
        self.pb_back_clean.clicked.connect(partial(self.stacked_clean.setCurrentIndex, 0))

    def _clear_tree_report(self):
        """Clean tree structure of report."""
        self.tree_report.clear()
        self.top_cleaned = QTreeWidgetItem([self.tr('Cleaned: 0'), '', '', ''])
        self.top_error = QTreeWidgetItem([self.tr('Error: 0'), '', '', ''])
        self.top_clean = QTreeWidgetItem([self.tr('Clean: 0'), '', '', ''])
        self.tree_report.addTopLevelItem(self.top_cleaned)
        self.tree_report.addTopLevelItem(self.top_error)
        self.tree_report.addTopLevelItem(self.top_clean)
        self.tree_report.itemDoubleClicked.connect(self._item_double_clicked)
        header = self.tree_report.headerItem()
        header.setToolTip(REP_COL_PLUGIN, self.tr('Double click on item to copy plugin`s path.'))
        header.setToolTip(REP_COL_TIME, self.tr('Cleaning time in min:sec\nHold on item to see cleaning details.'))

    def _add_report_data(self, plug: Path, result: bool, reason: str, cleaning_time: float, out: str, err: str):
        """
        Add data to report page.

        :param plug: path to plugin
        :param result: result
        :param reason: reason as string
        :param cleaning_time: cleaning time in seconds
        :param out: command output
        :param err: command error
        """
        error_txt = '\n'.join(reason.split('**'))
        if 'not found' in reason:
            reason = 'missing esm'
        item = QTreeWidgetItem([plug.name, reason, f'{utils.get_string_duration(cleaning_time)}'])
        item.setToolTip(REP_COL_PLUGIN, f'{plug}')
        item.setToolTip(REP_COL_TIME, f'{out.strip()}\n{err.strip()}')
        if result:
            self._report_icon_update_plugin_number(top_item=self.top_cleaned, child_item=item, icon=qtawesome.icon('fa5s.check', color='green'))
        elif not result and reason == 'not modified':
            self._report_icon_update_plugin_number(top_item=self.top_clean, child_item=item, icon=qtawesome.icon('fa5s.check', color='green'))
        elif not result and 'missing esm' in reason:
            self._report_icon_update_plugin_number(top_item=self.top_error, child_item=item, icon=qtawesome.icon('fa5s.times', color='red'), tip_text=error_txt)

    def _report_icon_update_plugin_number(self, top_item: QTreeWidgetItem, child_item: QTreeWidgetItem, icon: QIcon, tip_text: str = ''):
        """
        Update icon for plugin in report page.

        :param top_item: parent item
        :param child_item: child item
        :param icon: icon instance
        :param tip_text: tool tip text
        """
        child_item.setIcon(REP_COL_STATUS, icon)
        if tip_text:
            child_item.setToolTip(REP_COL_STATUS, tip_text)
        top_item.addChild(child_item)
        top_text = top_item.text(REP_COL_PLUGIN).split(' ')
        top_item.setText(REP_COL_PLUGIN, f'{top_text[0]} {int(top_text[1]) + 1}')
        self.tree_report.expandItem(top_item)

    def _item_double_clicked(self, item: QTreeWidgetItem) -> None:
        """
        Copy tool tip text of first column of clicked tree item to clipboard.

        :param item: item clicked
        """
        if item.parent():
            QApplication.clipboard().setText(item.toolTip(REP_COL_PLUGIN))
            self.statusbar.showMessage(self.tr('Path of plugin copied to clipboard'))

    # <=><=><=><=><=><=><=><=><=><=><=> omwcmd masters <=><=><=><=><=><=><=><=><=><=><=>
    def _init_omwcmd_masters(self):
        """Initialize events for omwcmd masters."""
        self.le_masters_plugin.textChanged.connect(partial(self._is_plugin_exists, widget_name='le_masters_plugin'))
        self.pb_masters_run.clicked.connect(self._masters_run)
        self.pb_masters_select.clicked.connect(partial(self._run_file_dialog, for_load=True, for_dir=False,
                                               last_dir=lambda: self.last_dir['le_masters_plugin'], widget_name='le_masters_plugin'))
        self.le_masters_plugin.textChanged.connect(self.trigger_autosave)

    def _is_plugin_exists(self, text: str, widget_name: str | None = None) -> None:
        """
        Check if plugin exists.

        :param text: path to plugin
        :param widget_name: QLineEdit widget name
        """
        file_exists = Path(text).is_file()
        self.logger.debug(f'Path: {text} for {widget_name} exists: {file_exists}')
        if file_exists:
            getattr(self, widget_name).setStyleSheet('')
            self.last_dir[widget_name] = str(Path(text).resolve().parent)
            self.pb_masters_run.setEnabled(True)
        else:
            getattr(self, widget_name).setStyleSheet('color: red;')
            self.pb_masters_run.setEnabled(False)

    def _masters_run(self):
        """Run omwcmd masters command."""
        out, _ = utils.run_cmd(f'{self.omwcmd} masters "{self.le_masters_plugin.text()}"')
        self.l_masters_result.setText(out)

    # <=><=><=><=><=><=><=><=><=><=><=> configuration <=><=><=><=><=><=><=><=><=><=><=>
    def load_config(self) -> None:
        """Load GUI configuration."""
        self.statusbar.showMessage('Choose configuration file')
        self.last_dir['cfg_dir'] = self.last_dir['cfg_dir'] if self.last_dir['cfg_dir'] else str(Path.home())
        conf_file = self._run_file_dialog(for_load=True, for_dir=False,
                                          last_dir=lambda: self.last_dir['cfg_dir'], file_filter='Yaml Files [*.yaml *.yml](*.yaml *.yml)')
        self.last_dir['cfg_dir'] = str(Path(conf_file).resolve().parent)
        if conf_file:
            self.conf_file = conf_file
            self._apply_gui_configuration(yamlfile=self.conf_file)
            self.statusbar.showMessage(f'Configuration loaded: {self.conf_file}')

    def save_config(self) -> None:
        """Save GUI configuration."""
        if not self.conf_file:
            self.statusbar.showMessage('Choose configuration file')
            self.last_dir['cfg_dir'] = self.last_dir['cfg_dir'] if self.last_dir['cfg_dir'] else str(Path.home())
            self.conf_file = self._run_file_dialog(for_load=False, for_dir=False,
                                                   last_dir=lambda: self.last_dir['cfg_dir'], file_filter='Yaml Files [*.yaml *.yml](*.yaml *.yml)')
            self.last_dir['cfg_dir'] = str(Path(self.conf_file).resolve().parent)
        try:
            self.config = self._dump_gui_configuration()
            write_config(self.config, self.conf_file)
            self.statusbar.showMessage(f'Configuration saved: {self.conf_file}')
        except OSError:
            self.cb_auto_save.setChecked(False)
            self.statusbar.showMessage('Configuration not saved')

    def save_config_as(self) -> None:
        """Save as GUI configuration."""
        self.conf_file = ''
        self.save_config()

    def _apply_gui_configuration(self, yamlfile: str) -> None:
        """
        Apply configuration from internal dict to GUI widgets.

        :param yamlfile: absolute path to configuration yaml
        """
        self.config = read_config(yamlfile)
        if self.config.get('moht', {}).get('auto_save', False):
            self.cb_auto_save.toggled.disconnect()
            self.auto_save = True
            self.config['moht']['auto_save'] = False
        try:
            self._apply_cfg_section()
        except (AttributeError, KeyError):
            self.config = read_config(Path(__file__) / 'default.yaml')
            self.conf_file = ''
            self._apply_cfg_section()
        if self.auto_save:
            self.config['moht']['auto_save'] = True
            self.cb_auto_save.setChecked(True)
            self.cb_auto_save.toggled.connect(self.autosave_toggled)

    def _apply_cfg_section(self) -> None:
        """Cycle thru config sections and apply configuration to GUI."""
        for cfg_section in self.config:
            getattr(self, f'_apply_cfg_{cfg_section}')(self.config[cfg_section])

    def _apply_cfg_moht(self, cfg_dict: dict[str, str | int | bool]) -> None:
        """
        Apply configuration of Moht.

        :param cfg_dict: configuration dict
        """
        self.logger.debug(f'Apply configuration for API ver: {cfg_dict["api_ver"]}')
        self.cb_auto_save.setChecked(cfg_dict['auto_save'])

    def _apply_cfg_tes3cmd_clean(self, cfg_dict: dict[str, str | int | bool]) -> None:
        """
        Apply configuration of tes3cmd.

        :param cfg_dict: configuration dict
        """
        mod_dir = cfg_dict['mod_dir']
        data_files = cfg_dict['data_files_dir']
        tes3bin = cfg_dict['tes3cmd_bin']
        tes_ver = cfg_dict['tes3cmd_ver']
        self.mods_dir = Path(mod_dir) if mod_dir else Path.home()
        self.morrowind_dir = Path(data_files) if data_files else Path.home()
        self.tes3cmd = Path(tes3bin) if tes3bin else MohtQtGui._set_executable_path(TES3CMD[platform][tes_ver])
        self.tes3cmd_ver = tes_ver
        self.cb_rm_backup.setChecked(cfg_dict['clean_backup'])
        self.cb_rm_cache.setChecked(cfg_dict['clean_cache'])

    def _apply_cfg_omwcmd_masters(self, cfg_dict: dict[str, str | int | bool]) -> None:
        """
        Apply configuration of omwcmd masters.

        :param cfg_dict:
        """
        omwcmd = cfg_dict['omwcmd_bin']
        self.omwcmd = Path(omwcmd) if omwcmd else MohtQtGui._set_executable_path(OMWCMD[platform])
        self.le_masters_plugin.setText(cfg_dict['plugin'])

    def _dump_gui_configuration(self) -> dict[str, dict[str, str | int | bool]]:
        """
        Dump GUI configuration to python dict.

        :return: GUI configuration as dict
        """
        c = {
            'moht': {
                'api_ver': VERSION,
                'auto_save': self.cb_auto_save.isChecked()
            },
            'tes3cmd_clean': {
                'mod_dir': str(self.mods_dir),
                'data_files_dir': str(self.morrowind_dir),
                'tes3cmd_bin': str(self.tes3cmd),
                'tes3cmd_ver': self.tes3cmd_ver,
                'clean_backup': self.cb_rm_backup.isChecked(),
                'clean_cache': self.cb_rm_cache.isChecked(),
            },
            'omwcmd_masters': {
                'omwcmd_bin': str(self.omwcmd),
                'plugin': self.le_masters_plugin.text(),
            },
        }
        return c

    # <=><=><=><=><=><=><=><=><=><=><=> helpers <=><=><=><=><=><=><=><=><=><=><=>
    def activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """
        Signal of activation.

        :param reason: reason of activation
        """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()

    def trigger_autosave(self) -> None:
        """Just trigger save configuration if auto save checkbox is checked."""
        if self.cb_auto_save.isChecked():
            self.save_config()

    @staticmethod
    def _set_executable_path(bin_file: str) -> Path:
        """
        Set path of executable fine.

        :param bin_file: file name
        :return: full absolute path
        """
        return Path(__file__).resolve().with_name('resources') / bin_file

    def check_updates(self) -> None:
        """Check for updates and show result."""
        _, desc = utils.is_latest_ver(package='moht', current_ver=VERSION)
        self.statusbar.showMessage(self.tr('ver. {0} - {1}').format(VERSION, desc))

    def run_in_background(self, job: partial | Callable, signal_handlers: dict[str, Callable]) -> None:
        """
        Worker with signals callback to schedule GUI job in background.

        signal_handlers parameter is a dict with signals from  WorkerSignals,
        possibles signals are: finished, error, result, progress. Values in dict
        are methods/callables as handlers/callbacks for particular signal.

        :param job: GUI method or function to run in background
        :param signal_handlers: signals as keys: finished, error, result, progress and values as callable
        """
        progress = True if 'progress' in signal_handlers.keys() else False
        worker = Worker(func=job, with_progress=progress)
        for signal, handler in signal_handlers.items():
            getattr(worker.signals, signal).connect(handler)
        if isinstance(job, partial):
            job_name = job.func.__name__
            args = job.args
            kwargs = job.keywords
        else:
            job_name = job.__name__
            args = tuple()
            kwargs = dict()
        signals = {signal: handler.__name__ for signal, handler in signal_handlers.items()}
        self.logger.debug(f'bg job for: {job_name} args: {args} kwargs: {kwargs} signals {signals}')
        self.threadpool.start(worker)

    def _set_icons(self, button: str | None = None, icon_name: str | None = None, color: str = 'black', spin: bool = False):
        """
        Universal method to set icon for QPushButtons.

        When button is provided without icon_name, current button icon will be removed.
        When none of button nor icon_name are provided, default starting icons are set for all buttons.

        :param button: button name
        :param icon_name: ex: spinner, check, times, pause
        :param color: ex: red, green, black
        :param spin: spinning icon: True or False
        """
        if not (button or icon_name):
            self.pb_mods_dir.setIcon(qtawesome.icon('fa5s.folder', color='brown'))
            self.pb_morrowind_dir.setIcon(qtawesome.icon('fa5s.folder', color='brown'))
            self.pb_tes3cmd.setIcon(qtawesome.icon('fa5s.file', color='brown'))
            self.pb_clean.setIcon(qtawesome.icon('fa5s.snowplow', color='brown'))
            self.pb_report.setIcon(qtawesome.icon('fa5s.file-contract', color='brown'))
            self.pb_back_clean.setIcon(qtawesome.icon('fa5s.arrow-left', color='brown'))
            self.pb_masters_select.setIcon(qtawesome.icon('fa5s.folder', color='brown'))
            self.pb_masters_run.setIcon(qtawesome.icon('fa5s.play', color='brown'))
            return
        btn = getattr(self, button)  # type: ignore
        if spin and icon_name:
            icon = qtawesome.icon(f'{icon_name}', color=color, animation=qtawesome.Spin(btn, 2, 1))
        elif not spin and icon_name:
            icon = qtawesome.icon(f'{icon_name}', color=color)
        else:
            icon = QIcon()
        btn.setIcon(icon)

    def _run_file_dialog(self, for_load: bool, for_dir: bool, last_dir: Callable[..., str],
                         widget_name: str | None = None, file_filter: str = 'All Files [*.*](*.*)') -> str:
        """
        Open/save dialog to select file or folder.

        :param for_load: if True show window for load, for save otherwise
        :param for_dir: if True show window for selecting directory only, if False selecting file only
        :param last_dir: function return last selected dir
        :param widget_name: update text for widget
        :param file_filter: list of types of files ;;-seperated: Text [*.txt](*.txt)
        :return: full path to file or directory
        """
        result_path = ''
        if file_filter != 'All Files [*.*](*.*)':
            file_filter = f'{file_filter};;All Files [*.*](*.*)'
        if for_load and for_dir:
            result_path = QFileDialog.getExistingDirectory(self, caption='Open Directory', directory=last_dir(),
                                                           options=QFileDialog.Option.ShowDirsOnly)
        if for_load and not for_dir:
            result_path = QFileDialog.getOpenFileName(self, caption='Open File', directory=last_dir(),
                                                      filter=file_filter, options=QFileDialog.Option.ReadOnly)[0]
        if not for_load and not for_dir:
            result_path = QFileDialog.getSaveFileName(self, caption='Save File', directory=last_dir(),
                                                      filter=file_filter, options=QFileDialog.Option.ReadOnly)[0]
        if widget_name is not None and result_path:
            getattr(self, widget_name).setText(result_path)
        return result_path

    def _show_message_box(self, kind_of: str, title: str, message: str = '') -> None:
        """
        Show any QMessageBox delivered with Qt.

        :param kind_of: any of: information, question, warning, critical, about or aboutQt
        :param title: Title of modal window
        :param message: text of message, default is empty
        """
        message_box = getattr(QMessageBox, kind_of)
        if kind_of == 'aboutQt':
            message_box(self, title)
        else:
            message_box(self, title, message)

    @staticmethod
    def _report_issue():
        """Open report issue web page in default browser."""
        webbrowser.open('https://gitlab.com/modding-openmw/modhelpertool/issues', new=2)

    def _find_children(self) -> None:
        """Fine all children of widgets."""
        self.statusbar: object | QStatusBar = self.findChild(QStatusBar, 'statusbar')
        self.progressbar: object | QProgressBar = self.findChild(QProgressBar, 'progressbar')
        self.systray: object | QSystemTrayIcon = self.findChild(QSystemTrayIcon, 'systray')
        self.traymenu: object | QMenu = self.findChild(QMenu, 'traymenu')

        # <=><=><=><=><=><=><=><=><=><=><=> tes3cmd <=><=><=><=><=><=><=><=><=><=><=>
        self.actionLoad: object | QAction = self.findChild(QAction, 'actionLoad')
        self.actionSave: object | QAction = self.findChild(QAction, 'actionSave')
        self.actionSave_as: object | QAction = self.findChild(QAction, 'actionSave_as')
        self.actionQuit: object | QAction = self.findChild(QAction, 'actionQuit')
        self.actionAboutMoht: object | QAction = self.findChild(QAction, 'actionAboutMoht')
        self.actionAboutQt: object | QAction = self.findChild(QAction, 'actionAboutQt')
        self.actionReportIssue: object | QAction = self.findChild(QAction, 'actionReportIssue')
        self.actionCheckUpdates: object | QAction = self.findChild(QAction, 'actionCheckUpdates')

        self.pb_mods_dir: object | QPushButton = self.findChild(QPushButton, 'pb_mods_dir')
        self.pb_morrowind_dir: object | QPushButton = self.findChild(QPushButton, 'pb_morrowind_dir')
        self.pb_tes3cmd: object | QPushButton = self.findChild(QPushButton, 'pb_tes3cmd')
        self.pb_report: object | QPushButton = self.findChild(QPushButton, 'pb_report')
        self.pb_back_clean: object | QPushButton = self.findChild(QPushButton, 'pb_back_clean')
        self.pb_clean: object | QPushButton = self.findChild(QPushButton, 'pb_clean')

        self.cb_rm_backup: object | QCheckBox = self.findChild(QCheckBox, 'cb_rm_backup')
        self.cb_rm_cache: object | QCheckBox = self.findChild(QCheckBox, 'cb_rm_cache')
        self.cb_auto_save: object | QCheckBox = self.findChild(QCheckBox, 'cb_auto_save')

        self.le_mods_dir: object | QLineEdit = self.findChild(QLineEdit, 'le_mods_dir')
        self.le_morrowind_dir: object | QLineEdit = self.findChild(QLineEdit, 'le_morrowind_dir')
        self.le_tes3cmd: object | QLineEdit = self.findChild(QLineEdit, 'le_tes3cmd')

        self.rb_40: object | QRadioButton = self.findChild(QRadioButton, 'rb_40')
        self.rb_37: object | QRadioButton = self.findChild(QRadioButton, 'rb_37')
        self.rb_custom: object | QRadioButton = self.findChild(QRadioButton, 'rb_custom')

        self.stacked_clean: object | QStackedWidget = self.findChild(QStackedWidget, 'stacked_clean')
        self.tree_report: object | QTreeWidget = self.findChild(QTreeWidget, 'tree_report')

        # <=><=><=><=><=><=><=><=><=><=><=> omwcmd <=><=><=><=><=><=><=><=><=><=><=>
        self.pb_masters_select: object | QPushButton = self.findChild(QPushButton, 'pb_masters_select')
        self.pb_masters_run: object | QPushButton = self.findChild(QPushButton, 'pb_masters_run')
        self.le_masters_plugin: object | QLineEdit = self.findChild(QLineEdit, 'le_masters_plugin')
        self.l_masters_result: object | QLabel = self.findChild(QLabel, 'l_masters_result')

    # <=><=><=><=><=><=><=><=><=><=><=> property <=><=><=><=><=><=><=><=><=><=><=>
    @property
    def mods_dir(self) -> Path:
        """
        Get root of mods directory.

        :return: mods dir as string
        """
        return self.le_mods_dir.text()

    @mods_dir.setter
    def mods_dir(self, value: Path) -> None:
        """
        Set root of mods directory.

        :param value: mods dir as string
        """
        self.le_mods_dir.setText(str(value))

    @property
    def morrowind_dir(self) -> Path:
        """
        Get Morrowind Data Files directory.

        :return: morrowind dir as string
        """
        return Path(self.le_morrowind_dir.text())

    @morrowind_dir.setter
    def morrowind_dir(self, value: Path) -> None:
        """
        Set Morrowind Data Files directory.

        :param value: morrowind dir as string
        """
        self.le_morrowind_dir.setText(str(value))

    @property
    def tes3cmd(self) -> Path:
        """
        Get tes3cmd binary file path.

        :return: tes3cmd file as string
        """
        return Path(self.le_tes3cmd.text())

    @tes3cmd.setter
    def tes3cmd(self, value: Path) -> None:
        """
        Set tes3cmd binary file path.

        :param value: tes3cmd file as string
        """
        self.le_tes3cmd.setText(str(value))

    @property
    def tes3cmd_ver(self) -> str:
        """
        Get tes3cmd version RadioButton.

        :return: tes3cmd version as string
        """
        for ver in [37, 40, 'custom']:
            rb = getattr(self, f'rb_{ver}')
            if rb.isChecked():
                return ver

    @tes3cmd_ver.setter
    def tes3cmd_ver(self, value: str) -> None:
        """
        Set tes3cmd version RadioButton.

        :param value: tes3cmd version as string
        """
        try:
            getattr(self, f'rb_{value}').setChecked(True)
        except AttributeError:
            self.logger.debug(f'Can not change select: rb_{value}')


class AboutDialog(QDialog):
    """About dialog."""
    def __init__(self, parent) -> None:
        """Moht about dialog window."""
        super().__init__(parent)
        UiLoader().loadUi(':/ui/ui/about.ui', self)
        self.label: object | QLabel = self.findChild(QLabel, 'label')
        self.setup_text()

    def setup_text(self) -> None:
        """Prepare text information about Moht application."""
        log_path = Path(gettempdir()) / 'moht.log'
        text = self.label.text().rstrip('</body></html>')
        text += self.tr('<p>When report an issue please attach log:<br/>')
        text += f'{log_path}<br/><br/>'
        text += f'<b>moht</b>: {VERSION}'
        text += '<br><b>Python</b>: {}.{}.{}-{}.{}'.format(*version_info)
        text += f'<br><b>PySide6</b>: {pyside6_ver} / <b>Qt</b>: {qt6_ver}</p></body></html>'
        self.label.setText(text)


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:
    * finished - no data
    * error - tuple with exctype, value, traceback.format_exc()
    * result - object/any type - data returned from processing
    * progress - float between 0 and 1 as indication of progress
    """

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    """Runnable worker."""

    def __init__(self, func: partial, with_progress: bool) -> None:
        """
        Worker thread.

        Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
        :param func: The function callback to run on worker thread
        """
        super().__init__()
        self.func = func
        self.signals = WorkerSignals()
        if with_progress:
            self.func.keywords['progress_callback'] = self.signals.progress

    @Slot()
    def run(self) -> None:
        """Initialise the runner function with passed additional kwargs."""
        try:
            result = self.func()
        except Exception:
            exctype, value = exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class UiLoader(QUiLoader):
    """UI file loader."""
    _baseinstance = None

    def createWidget(self, classname: str, parent: QWidget | None = None, name='') -> QWidget:
        """
        Create widget.

        :param classname: class name
        :param parent: parent
        :param name: name
        :return: QWidget
        """
        if parent is None and self._baseinstance is not None:
            widget = self._baseinstance
        else:
            widget = super().createWidget(classname, parent, name)
            if self._baseinstance is not None:
                setattr(self._baseinstance, name, widget)
        return widget

    def loadUi(self, ui_path: str | bytes | Path, baseinstance=None) -> QWidget:
        """
        Load UI file.

        :param ui_path: path to UI file
        :param baseinstance:
        :return: QWidget
        """
        self._baseinstance = baseinstance
        ui_file = QFile(ui_path)
        ui_file.open(QIODevice.OpenModeFlag.ReadOnly)
        try:
            widget = self.load(ui_file)
            QMetaObject.connectSlotsByName(widget)
            return widget
        finally:
            ui_file.close()
