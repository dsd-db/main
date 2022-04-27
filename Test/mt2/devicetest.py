import os
import sys
import random

from initializate import rd,g,DEVICE
import db

if len(sys.argv)==1:
    COUNT=8192
else:
    COUNT=int(sys.argv[1])

a=dict()

def f(uuid):
    try:
        db.device.get(uuid,True)
    except ValueError:
        pass
    else:
        print(repr(uuid))
        assert ValueError==None

for _ in range(COUNT):
    if not _&255:
        print('db.device',_)
    i=random.randint(0,5)
    if i==0:
        j=random.randint(0,1)
        if j==0:
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
        j=random.randint(0,1)
        if j==0:
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
    elif i==2:
        j=random.randint(0,4)
        if j==0:
            id=g(rd('id'))
            while len(id.replace('-',''))==32:
                id=g(id)
            f(id)
        elif j==1:
            id=g(rd('id'),random.choice('0123456789abcdef'))
            f(id)
        elif j==2 or j==3:
            id=g(g(rd('id')),random.choice('ghijklmnopqrstuvwxyzGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*,./:;<=>?@[\\]^`{|}~'))
            f(id)
        elif j==4:
            id=''
            f(id)
    else:
        if not a:
            continue
        id=random.choice(list(a.keys()))
        j=random.randint(0,1)
        if j==0:
            d=db.device.get(id,True)
        else:
            d=db.device.get(id)
        assert d!=None
        assert d.banned==a[id]['banned']
        assert d.email==a[id]['email']
        assert d.model==a[id]['model']
        assert d.calibration==a[id]['calibration']
        k=random.randint(0,15)
        if k&1:
            a[id]['banned']=not a[id]['banned']
            d.banned=a[id]['banned']
            assert d.banned==a[id]['banned']
        if k&2:
            a[id]['email']=rd('email')
            d.email=a[id]['email']
            assert d.email==a[id]['email']
        if k&4:
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
        if k&8:
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
