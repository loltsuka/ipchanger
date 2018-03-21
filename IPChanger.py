#!/usr/bin/env python3
#IPChanger.py

import os
import subprocess
import sys
from PyQt4 import QtGui, QtCore
from window_module import Window

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

def create_shortcut():
    if 'shortcutter.desktop' not in os.listdir():
        with open('shortcutter.desktop', 'w') as f:
            f.write('[Desktop Entry]\n')
            f.write('Name=Test\n')
            f.write('Exec='+os.path.abspath(__file__)+'\n')
            f.write('Icon='+os.path.abspath(__file__)[:-13]+'/Thinking.png\n')
            f.write('Terminal=false\n')
            f.write('Type=Application\n')
            f.write('Name[en_US]=IPChanger\n')

create_shortcut()
run()

