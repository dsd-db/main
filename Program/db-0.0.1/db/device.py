import os
import shutil

from db.__config import device,flushdevice,MODEL,CALIBRATION

def get(uuid:str,create:bool=False):
    if create and uuid not in device:
        device[uuid]={
            'uuid':uuid,
            'banned':False,
            'email':None,
            'model':MODEL%uuid,
            'calibration':CALIBRATION%uuid,
        }
        os.makedirs(device[uuid]['calibration'])
        flushdevice()
    if uuid in device:
        return Device(uuid)

def remove(uuid:str)->None:
    if uuid in device:
        shutil.rmtree(os.path.dirname(device[uuid]['model']))
        del device[uuid]
        flushdevice()

class Device:
    def __init__(
        self,
        uuid:str,
    )->None:
        self.uuid=uuid

    @property
    def banned(self)->bool:
        return device[self.uuid]['banned']
    
    @banned.setter
    def banned(self,value:bool)->None:
        device[self.uuid]['banned']=value
        flushdevice()

    @property
    def email(self)->str:
        return device[self.uuid]['email']

    @email.setter
    def email(self,value:str)->None:
        device[self.uuid]['email']=value
        flushdevice()

    @property
    def model(self)->str:
        if os.path.exists(device[self.uuid]['model']):
            return device[self.uuid]['model']

    @model.setter
    def model(self,value:str)->None:
        os.rename(value,device[self.uuid]['model'])

    @property
    def calibration(self)->str:
        if os.listdir(device[self.uuid]['calibration']):
            return device[self.uuid]['calibration']

    @calibration.setter
    def calibration(self,value:str)->None:
        shutil.rmtree(device[self.uuid]['calibration'])
        os.rename(value,device[self.uuid]['calibration'])
