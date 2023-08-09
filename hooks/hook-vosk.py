from PyInstaller.utils.hooks import collect_all


def hook(hook_api):
    datas, binaries, hiddenimports = collect_all('torch')
    hook_api.add_datas(datas)  # Comment out because it is usually not used
    #hook_api.add_binaries(binaries)
    hook_api.add_imports(*hiddenimports)


    packages = ['vosk','image','torchvision','torchaudio','nemo','pytorch_lightning',
                'rich','tqdm','regex','requests','transformers','packaging',
                'filelock','numpy','tokenizers','lightning_fabric','lightning_utilities','scipy',
                'librosa','sklearn', 'ipadic', 'whisper', 'langcodes', 'language_data', 'jsonpickle','win32timezone',
                'huggingface_hub','safetensors','encodings','importlib',
                'pyyaml']
    for package in packages:
        datas, binaries, hiddenimports = collect_all(package)
        #yprint(datas)
        #print(binaries)
        #print(hiddenimports)
        hook_api.add_datas(datas)  # Comment out because it is usually not used
        hook_api.add_binaries(binaries)
        hook_api.add_imports(*hiddenimports)

"""
packages = ['vosk','image','torchvision','torchaudio','nemo','pytorch_lightning',
                'rich','tqdm','regex','requests','transformers','packaging',
                'filelock','numpy','tokenizers','lightning_fabric','lightning_utilities','scipy',
                'librosa','sklearn', 'ipadic', 'whisper', 'langcodes', 'language_data', 'jsonpickle','win32timezone','encodings']
"""