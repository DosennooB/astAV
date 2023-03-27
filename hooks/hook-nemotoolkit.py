from PyInstaller.utils.hooks import collect_all

def hook(hook_api):
    packages = ['nemo-toolkit']
    for package in packages:
        datas, binaries, hiddenimports = collect_all(package)
        print(datas)
        print(binaries)
        print(hiddenimports)
        hook_api.add_datas(datas)  # Comment out because it is usually not used
        hook_api.add_binaries(binaries)
        hook_api.add_imports(*hiddenimports)