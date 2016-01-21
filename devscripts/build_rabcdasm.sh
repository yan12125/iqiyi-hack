#!/bin/bash
git clone git://github.com/CyberShadow/RABCDAsm.git ~/RABCDAsm
cd ~/RABCDAsm
dmd -run build_rabcdasm.d
