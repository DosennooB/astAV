import jsonpickle
import os
class Jsonpresetsave(object):
    @staticmethod
    def saveStask(preset_list: list, currentpreset: str)-> bool:
        path = 'config'
        path = os.path.join(path, 'preset_config.json')
        completdict = {}
        completdict.update({'_presetlist':preset_list})
        completdict.update({'_currentpreset': currentpreset})
        print(completdict)
        picklebel_object = jsonpickle.encode(completdict, unpicklable=True)
        try:
            f = open(path, "w")
            f.write(picklebel_object)
            f.close()
        except:
            pass
            #TODO

    @staticmethod
    def readStask()-> [list, str]:
        preset_list = []
        currentpreset = ''
        path = 'config'
        path = os.path.join(path, 'preset_config.json')
        try:
            f = open(path, "r")
            preset_str =  f.read()
            f.close()
            complet_dict = jsonpickle.decode(preset_str)
            preset_list = complet_dict['_presetlist']
            currentpreset = complet_dict['_currentpreset']

        except Exception as e:
            print(e.with_traceback())
        return [preset_list,currentpreset]

