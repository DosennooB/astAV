import jsonpickle
import os
class Jsonlanguagesave(object):
    @staticmethod
    def saveLanguage(lang: str)-> bool:
        path = 'config'
        path = os.path.join(path,'language_config.json')
        pickle_object = jsonpickle.encode(lang)
        try:
            f = open(path, "w")
            f.write(pickle_object)
            f.close()
        except:
            pass
            #TODO

    @staticmethod
    def readLanguage()-> str:
        lang = ''
        path = 'config'
        path = os.path.join(path, 'language_config.json')
        try:
            f = open(path, "r")
            lang_str = f.read()
            f.close()
            lang = jsonpickle.decode(lang_str)
        except:
            pass
        return lang