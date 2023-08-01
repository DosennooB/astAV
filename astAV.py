#!/usr/bin/env python3


from src.config.configsupply import ConfigSupply
if __name__ == "__main__":
    ConfigSupply()

    from src.gui.gui import astAVGui
    astAVGui().run()