#!/usr/bin/env python3
"""
Launcher pour Music Player
Change le répertoire courant et lance main.py
"""

import os
import sys
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)

if __name__ == '__main__':
    sys.path.insert(0, script_dir)
    
    import main
