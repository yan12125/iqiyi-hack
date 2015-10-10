# iqiyi-hack

Inspired by https://github.com/soimort/you-get/pull/655

## Features:
* No need to use the debug version of flash players
* Cross platform. Tested on Arch Linux

## Dependencies
* rabcdasm
* Python 3
* Firefox
* Selenium

On Arch Linux, the following command is sufficient:
```
yaourt -S --needed rabcdasm-git python firefox freshplayerplugin-git chromium-pepper-flash python-selenium
```

## Usage
1. cd src/
2. python3 get\_swf.py
3. The key will be printed in the console
