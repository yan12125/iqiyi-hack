# iqiyi-hack

[![Build Status](https://travis-ci.org/yan12125/iqiyi-hack.svg?branch=master)](https://travis-ci.org/yan12125/iqiyi-hack)

Inspired by https://github.com/soimort/you-get/pull/655

## Features:
* No need to use the debug version of flash players
* Cross platform. Tested on Arch Linux

## Dependencies
* rabcdasm
* Python 2 or Python 3
* Firefox
* Selenium
* PyVirtualDisplay (optional, enables running without an actual X server)
* python-patch

On Arch Linux, the following command is sufficient:
```
yaourt -S --needed rabcdasm-git python-pip firefox freshplayerplugin-git chromium-pepper-flash
pip install --user -r requirements.txt
```

## Usage
1. cd src/
2. python3 get\_swf.py iqiyi
3. The key will be printed in the console

To hack letv key, replace iqiyi with letv in the second command
