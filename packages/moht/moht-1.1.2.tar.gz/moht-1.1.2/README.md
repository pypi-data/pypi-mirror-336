[![pipeline status](https://gitlab.com/modding-openmw/modhelpertool/badges/main/pipeline.svg)](https://gitlab.com/modding-openmw/modhelpertool/-/commits/main)
[![coverage report](https://gitlab.com/modding-openmw/modhelpertool/badges/main/coverage.svg)](https://gitlab.com/modding-openmw/modhelpertool/-/commits/main)
[![image](https://img.shields.io/badge/pypi-v1.1.2-blue.svg)](https://pypi.org/project/moht/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](./LICENSE.md)
[![image](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://gitlab.com/modding-openmw/modhelpertool)
[![release](https://gitlab.com/modding-openmw/modhelpertool/-/badges/release.svg)](https://gitlab.com/modding-openmw/modhelpertool/-/releases)
[![moht](https://snyk.io/advisor/python/moht/badge.svg)](https://snyk.io/advisor/python/moht)

![mohtlogo](https://i.imgur.com/gJoB1Dv.png)

## Mod Helper Tool
Simple yet powerful tool to help you manage your mods in several ways.

## Name
MHT and MOTH was already occupied by another projects, so **MO**d **H**elper **T**ool, `MOHT` in short was born.
Anyway if you not pay attention to details or your english is not fluent (as mine) logo fits like a glove.

## General
For now, application can only clean your mods, but in future more features will be added.

* Run Linux, Windows and Mac (not tested)
* Multithreading capabilities
* Use `PySide6` as GUI framework
* Two built-in version `tes3cmd` binary (0.40 and 0.37) - no additional downloads needed
* Allow to select custom `tes3cmd` executable file
* Select location of directory with Mods
* Select location of `Morrowind/Data Files` directory
* Simple report after cleaning

## Requirements
* Python 3.10+ should be fine
* Linux users require install additional [Perl module](#perl-module)
* `pip` in any version but 22.2 grater is recommended (used to check new version of Moht)

## Installation
1. Any Python version grater the 3.10
   * Windows 10/11, during Python installation please select:
     * Optional Features:
       * pip
       * py launcher
     * Advanced Options:
       * Associate files with Python (requires the py launcher)
       * Add Python to environment variables
       * Customize install location: C:\Python312 or C:\Python

2. Package is available on [PyPI](https://pypi.org/project/moht/), open Windows Command Prompt (cmd.exe) or any terminal and type:
   ```shell
   pip install moht
   ```
3. You can drag and drop `moht.exe` to desktop and make shortcut (with custom icon, you can find icon in installation  directory i.e. C:\Python312\lib\site-packages\moht\img\moht.ico).

## Perl module
`perl-Config-IniFiles` is required for `tes3cmd-0.37` which Moht use to clean-up mods. Install with
  * Arch / Manjaro (AUR)
    ```shell
    sudo yay -S perl-config-inifiles
    ```
  * Gentoo
    ```shell
    sudo emerge dev-perl/Config-IniFiles
    ```
  * Debian / Ubuntu / Mint
    ```shell
    sudo apt install libconfig-inifiles-perl
    ```
  * OpenSUSE
    ```shell
    sudo zypper install perl-Config-IniFiles
    ```
  * Fedora / CentOS / RHEL
    ```shell
    sudo dnf install perl-Config-IniFiles.noarch
    ```
However, moht has v0.40 built-in as well which do not require perl package.

## Start
* Windows

  You can find executable(s) with little trick, open Windows Command Prompt (cmd.exe) and type:
  ```shell
  pip uninstall moht
  ```
  Note: answer **No** to question. It will show you, where Moht was installed. Usually pip should install moht into your Python directory: i.e.:
  ```
  C:\Python313\lib\site-packages\moht-1.1.2.dist-info\*
  C:\Python313\lib\site-packages\moht\*
  C:\Python313\scripts\moht.exe
  ```
* Linux

  Simply run `moht` from terminal

## Upgrade
To upgrade Moht to the latest version:
```shell
pip install -U moht
```

## Uninstall
```shell
pip install -qy moht
```

## Sponsored by Jetbrains Open Source Support Program
[![logo](https://resources.jetbrains.com/storage/products/company/brand/logos/PyCharm.svg)](https://jb.gg/OpenSourceSupport)
[![logo](https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.svg)](https://jb.gg/OpenSourceSupport)
