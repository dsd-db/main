import os
import shutil
import sqlite3
from uuid import UUID

from db.__config import DEVICE,MODEL,CALIBRATION
con=sqlite3.connect(DEVICE)
cur=con.cursor()
cur.execute('create table if not exists device(uuid varchar(64) primary key,banned boolean,email varchar(1024),model varchar(1024),calibration varchar(1024))')
con.commit()


def get(uuid:str,create:bool=False):
    cur.execute('select banned,email,model,calibration from device where uuid=?',(uuid,))
    info=cur.fetchone()

    # if create and uuid not in device:
    #     device[uuid]={
    #         'uuid':uuid,
    #         'banned':False,
    #         'email':None,
    #         'model':MODEL%uuid,
    #         'calibration':CALIBRATION%uuid,
    #     }
    #     os.makedirs(device[uuid]['calibration'])
    #     flushdevice()
    if create and not info:
        _model=MODEL%uuid
        _calibration=CALIBRATION%uuid
        cur.execute('insert into device(uuid,banned,email,model,calibration) values(?,?,?,?,?)',(uuid,False,None,_model,_calibration))
        con.commit()
        info=(0,None,_model,_calibration)
        os.makedirs(_calibration)

    # if uuid in device:
    #     return Device(uuid)
    if info:
        UUID(uuid,version=4)
        return Device(uuid)


def remove(uuid:str)->None:
    # if uuid in device:
    #     shutil.rmtree(os.path.dirname(device[uuid]['model']))
    #     del device[uuid]
    #     flushdevice()
    cur.execute('delete from device where uuid=?',(uuid,))
    _dir=os.path.dirname(CALIBRATION%uuid)
    if os.path.exists(_dir):
        shutil.rmtree(_dir)
    con.commit()


class Device:
    def __init__(
        self,
        uuid:str
    )->None:
        self.uuid=uuid

    @property
    def banned(self)->bool:
        # return self.banned
        cur.execute('select banned from device where uuid=?',(self.uuid,))
        return cur.fetchone()[0]
    
    @banned.setter
    def banned(self,value:bool)->None:
        # device[self.uuid]['banned']=value
        # flushdevice()
        cur.execute('update device set banned=? where uuid=?',(value,self.uuid))
        con.commit()

    @property
    def email(self)->str:
        # return device[self.uuid]['email']
        cur.execute('select email from device where uuid=?',(self.uuid,))
        return cur.fetchone()[0]

    @email.setter
    def email(self,value:str)->None:
        # device[self.uuid]['email']=value
        # flushdevice()
        cur.execute('update device set email=? where uuid=?',(value,self.uuid))
        con.commit()

    @property
    def model(self)->str:
        # if os.path.exists(device[self.uuid]['model']):
        #     return device[self.uuid]['model']
        # else:
        #     return None
        cur.execute('select model from device where uuid=?',(self.uuid,))
        s=cur.fetchone()[0]
        if os.path.exists(s):
            return s
        # else:
        #     return None

    @model.setter
    def model(self,value:str)->None:
        # os.rename(value,device[self.uuid]['model'])
        cur.execute('select model from device where uuid=?',(self.uuid,))
        s=cur.fetchone()[0]
        os.rename(value,s)


    @property
    def calibration(self)->str:
        # if os.listdir(device[self.uuid]['calibration']):
        #     return device[self.uuid]['calibration']
        # else:
        #     return None
        cur.execute('select calibration from device where uuid=?',(self.uuid,))
        s=cur.fetchone()[0]
        if os.listdir(s):
            return s
        # else:
        #     return None

    @calibration.setter
    def calibration(self,value:str)->None:
        # shutil.rmtree(device[self.uuid]['calibration'])
        # os.rename(value,device[self.uuid]['calibration'])
        cur.execute('select calibration from device where uuid=?',(self.uuid,))
        s=cur.fetchone()[0]
        shutil.rmtree(s)
        os.rename(value,s)
