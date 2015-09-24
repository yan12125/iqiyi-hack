# iqiyi-hack

Inspired by https://github.com/soimort/you-get/pull/655

## Features:
* No need to use the debug version of flash players
* Cross platform. Tested on Arch Linux

## Dependencies
* rabcdasm
* Python 3
* Browsers with a Flash player and PAC (Proxy auto-config) support

On Arch Linux, the following command is sufficient:
```
yaourt -S --needed rabcdasm-git python firefox freshplayerplugin-git chromium-pepper-flash
```

## Usage
1. cd src/
2. Download the iQiyi SWF player
3. Run ``./patch_swf.sh``
4. Run ``python server.py``
5. Open firefox and change the PAC URL to http://localhost:7000/proxy.pac
6. Load an iQiyi video
7. The key will be printed in STDOUT of server.py
