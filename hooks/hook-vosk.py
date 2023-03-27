from PyInstaller.utils.hooks import collect_all


def hook(hook_api):
    packages = ['vosk','torch','image','torchvision','torchaudio','nemo','pytorch_lightning',
                'rich','tqdm','regex','requests','transformers','packaging',
                'filelock','numpy','tokenizers','lightning_fabric','lightning_utilities','scipy',
                'librosa','sklearn', 'ipadic']
    for package in packages:
        datas, binaries, hiddenimports = collect_all(package)
        #yprint(datas)
        #print(binaries)
        print(hiddenimports)
        hook_api.add_datas(datas)  # Comment out because it is usually not used
        hook_api.add_binaries(binaries)
        hook_api.add_imports(*hiddenimports)