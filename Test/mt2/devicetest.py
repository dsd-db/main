import os
import sys
import random
from uuid import UUID

import db
from initializate import rd,g,DEVICE

if len(sys.argv)==1:
    COUNT=8192
else:
    COUNT=int(sys.argv[1])

a=dict()

def f(uuid):
    try:
        db.device.get(uuid,True)
        print(repr(uuid))
        assert False
    except ValueError:
        pass

for _ in range(COUNT):
    if not _&255:
        print('db.device',_)
    i=random.randint(0,5)
    if i==0: # db.device.remove
        j=random.randint(0,1)
        if j==0: # db.device.remove(not_exists_id)
            id=rd('id')
            db.device.remove(id)
        else: # db.device.remove(exists_id)
            if not a:
                continue
            id=random.choice(list(a.keys()))
            db.device.remove(id)
            del a[id]
            assert db.device.get(id,False)==None
            assert not os.path.exists(os.path.join(DEVICE,id))
    elif i==1: # db.device.get(not_exists_id)
        j=random.randint(0,1)
        if j==0: # db.device.get(not_exists_id,False)
            id=rd('id')
            assert db.device.get(id,False)==None
            assert not os.path.exists(os.path.join(DEVICE,id))
        else: # db.device.get(not_exists_id,True)
            id=rd('id')
            assert db.device.get(id,True)!=None
            a[id]={
                'id':UUID(id,version=4),
                'banned':False,
                'email':None,
                'model':None,
                'calibration':None,
            }
            assert os.path.exists(os.path.join(DEVICE,id))
    elif i==2: # db.device.get(illegal_id)
        j=random.randint(0,4)
        if j==0: # db.device.get(short_id)
            id=g(rd('id'))
            while len(id.replace('-',''))==32:
                id=g(id)
            f(id)
        elif j==1: # db.device.get(long_id)
            id=g(rd('id'),random.choice('0123456789abcdef'))
            f(id)
        elif j==2 or j==3: # db.device.get(id_with_illegal_char)
            id=g(g(rd('id')),random.choice('ghijklmnopqrstuvwxyzGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*,./:;<=>?@[\\]^`|~'))
            f(id)
        elif j==4: # db.device.get('')
            id=''
            f(id)
    else: # db.device.Device
        if not a:
            continue
        id=random.choice(list(a.keys()))
        j=random.randint(0,1)
        if j==0:
            d=db.device.get(id,True)
        else:
            d=db.device.get(id,False)
        assert d!=None
        assert str(d.id)==str(a[id]['id'])
        assert d.id.hex==a[id]['id'].hex
        assert d.banned==a[id]['banned']
        assert d.email==a[id]['email']
        assert d.model==a[id]['model']
        assert d.calibration==a[id]['calibration']
        k=random.randint(1,31)
        if k&1: # id
            try:
                d.id=''
                assert False
            except:
                pass
        if k&2: # banned
            a[id]['banned']=not a[id]['banned']
            d.banned=a[id]['banned']
            assert d.banned==a[id]['banned']
        if k&4: # email
            a[id]['email']=rd('email')
            d.email=a[id]['email']
            assert d.email==a[id]['email']
        if k&8: # model
            l=d.model
            if l:
                assert os.path.exists(l)

            m=rd('mdl')
            assert os.path.exists(m)

            d.model=m
            assert d.model!=m
            if l:
                assert d.model==l
            else:
                a[id]['model']=d.model
            assert d.model==a[id]['model']
            assert os.path.exists(m)
            assert os.path.exists(d.model)
        if k&16: # calibration
            l=d.calibration
            if l:
                assert os.listdir(l)

            c=rd('c')
            assert os.listdir(c)

            d.calibration=c
            assert d.calibration!=c
            if l:
                assert d.calibration==l
            else:
                a[id]['calibration']=d.calibration
            assert d.calibration==a[id]['calibration']
            assert os.listdir(c)
            assert os.listdir(d.calibration)

print('OK')
