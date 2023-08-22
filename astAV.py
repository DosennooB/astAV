#!/usr/bin/env python3
import sys, os
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

from src.config.configsupply import ConfigSupply
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    ConfigSupply()

    from src.gui.gui import astAVGui
    astAVGui().run()