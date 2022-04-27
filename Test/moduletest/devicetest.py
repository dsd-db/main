import os

from initializate import rd
import db

id1=rd('id')
id2=rd('id')
id3=rd('id')
assert id1!=id2 and id1!=id3 and id2!=id3
assert db.device.get(id1)==None
assert db.device.get(id2)==None
assert db.device.get(id3)==None

d1=db.device.get(id1,True)
assert d1.banned==False
assert d1.email==None
assert d1.model==None
assert d1.calibration==None

d2=db.device.get(id2,True)
assert d2.banned==False
assert d2.email==None
assert d2.model==None
assert d2.calibration==None

assert d1!=d2
assert db.device.get(id3)==None

db.device.remove(id3)
assert db.device.get(id3)==None

e1=rd('email')
e2=rd('email')
e3=rd('email')
m1=rd('mdl')
m2=rd('mdl')
m3=rd('mdl')
c1=rd('c')
c2=rd('c')
c3=rd('c')
assert e1!=e2 and e1!=e3 and e2!=e3
assert m1!=m2 and m1!=m3 and m2!=m3
assert c1!=c2 and c1!=c3 and c2!=c3
assert os.path.exists(m1)
assert os.path.exists(m2)
assert os.path.exists(m3)
assert os.listdir(c1)
assert os.listdir(c2)
assert os.listdir(c3)

d1.email=e1
d1.model=m1
d1.calibration=c1
assert d1.banned==False
assert d1.email==e1
assert d2.banned==False
assert d2.email==None
assert d2.model==None
assert d2.calibration==None
assert not os.path.exists(m1)
assert os.path.exists(m2)
assert os.path.exists(m3)
assert not os.path.exists(c1)
assert os.listdir(c2)
assert os.listdir(c3)

r_m1=d1.model
assert os.path.exists(r_m1)
r_c1=d1.calibration
assert os.listdir(r_c1)

d2.email=e2
d2.model=m2
d2.calibration=c2
assert d1.banned==False
assert d1.email==e1
assert d2.banned==False
assert d2.email==e2
assert not os.path.exists(m1)
assert not os.path.exists(m2)
assert os.path.exists(m3)
assert not os.path.exists(c1)
assert not os.path.exists(c2)
assert os.listdir(c3)

r_m2=d2.model
assert os.path.exists(r_m2)
r_c2=d2.calibration
assert os.listdir(r_c2)

d1.email=e3
d1.model=m3
d1.calibration=c3
assert d1.banned==False
assert d1.email==e3
assert d2.banned==False
assert d2.email==e2
assert not os.path.exists(m1)
assert not os.path.exists(m2)
assert not os.path.exists(m3)
assert not os.path.exists(c1)
assert not os.path.exists(c2)
assert not os.path.exists(c3)

assert d1.model==r_m1
assert d1.calibration==r_c1

assert os.path.exists(r_m1)
assert os.listdir(r_c1)
assert os.path.exists(r_m2)
assert os.listdir(r_c2)

d1.banned=True
assert d1.banned==True
assert d2.banned==False

db.device.remove(id1)
assert not os.path.exists(r_m1)
assert not os.path.exists(r_c1)
assert os.path.exists(r_m2)
assert os.listdir(r_c2)
assert db.device.get(id1)==None
assert db.device.get(id2)!=None
assert db.device.get(id3)==None

assert db.device.get(id1,True)!=None

id4=rd('id')+'0'
try:
    db.device.get(id4,True)
except ValueError:
    pass
else:
    assert ValueError==None

print('OK')
