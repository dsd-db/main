import os
import sys
import random

from initializate import rd,DEVICE
import db

if len(sys.argv)==1:
    COUNT=8192
else:
    COUNT=int(sys.argv[1])

a=dict()

for _ in range(COUNT):
    if not _&255:
        print('db.device',_)
    i=random.randint(0,5)
    if i==0:
        i=random.randint(0,1)
        if i==0:
            id=rd('id')
            db.device.remove(id)
        else:
            if not a:
                continue
            id=random.choice(list(a.keys()))
            db.device.remove(id)
            del a[id]
            assert db.device.get(id)==None
            assert not os.path.exists(os.path.join(DEVICE,id))
    elif i==1:
        i=random.randint(0,1)
        if i==0:
            id=rd('id')
            assert db.device.get(id)==None
            assert not os.path.exists(os.path.join(DEVICE,id))
        else:
            id=rd('id')
            assert db.device.get(id,True)!=None
            a[id]={
                'banned':False,
                'email':None,
                'model':None,
                'calibration':None,
            }
            assert os.path.exists(os.path.join(DEVICE,id))
    else:
        if not a:
            continue
        id=random.choice(list(a.keys()))
        i=random.randint(0,1)
        if i==0:
            d=db.device.get(id,True)
        else:
            d=db.device.get(id)
        assert d!=None
        assert d.banned==a[id]['banned']
        assert d.email==a[id]['email']
        assert d.model==a[id]['model']
        assert d.calibration==a[id]['calibration']
        i=random.randint(0,15)
        if i&1:
            a[id]['banned']=not a[id]['banned']
            d.banned=a[id]['banned']
            assert d.banned==a[id]['banned']
        if i&2:
            a[id]['email']=rd('email')
            d.email=a[id]['email']
            assert d.email==a[id]['email']
        if i&4:
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
            assert not os.path.exists(m)
            assert os.path.exists(d.model)
        if i&8:
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
            assert not os.path.exists(c)
            assert os.listdir(d.calibration)

print('OK')
