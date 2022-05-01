import shutil

from db.__config import BASE

def getBase()->str:
    return BASE

def setBase(path:str)->None:
    shutil.copyfile(path,BASE)
