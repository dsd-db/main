import os
from uuid import UUID

import db
from initializate import rd

id1=rd('id')
id2=rd('id')
id3=rd('id')
assert id1!=id2 and id1!=id3 and id2!=id3
assert db.device.get(id1,False)==None
assert db.device.get(id2,False)==None
assert db.device.get(id3,False)==None

d1=db.device.get(id1,True)
assert id1==d1.id.hex
assert d1.banned==False
assert d1.email==None
assert d1.model==None
assert d1.calibration==None

d2=db.device.get(id2,True)
assert id2==d2.id.hex
assert d2.banned==False
assert d2.email==None
assert d2.model==None
assert d2.calibration==None

try:
    d1.id=''
    assert False
except:
    pass

assert d1!=d2
assert db.device.get(id3,False)==None

db.device.remove(id3)
assert db.device.get(id3,False)==None

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
assert os.path.exists(m1)
assert os.path.exists(m2)
assert os.path.exists(m3)
assert os.listdir(c1)
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
assert os.path.exists(m1)
assert os.path.exists(m2)
assert os.path.exists(m3)
assert os.listdir(c1)
assert os.listdir(c2)
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
assert os.path.exists(m1)
assert os.path.exists(m2)
assert os.path.exists(m3)
assert os.listdir(c1)
assert os.listdir(c2)
assert os.listdir(c3)

assert d1.model==r_m1
assert d1.calibration==r_c1

assert os.path.exists(r_m1)
assert os.listdir(r_c1)
assert os.path.exists(r_m2)
assert os.listdir(r_c2)

d1.banned=True
assert d1.banned==True
assert d2.banned==False

try:
    d1.email='a'*254+'@t.me'
    assert False
except ValueError:
    pass

db.device.remove(id1)
assert not os.path.exists(r_m1)
assert not os.path.exists(r_c1)
assert os.path.exists(r_m2)
assert os.listdir(r_c2)
assert db.device.get(id1,False)==None
assert db.device.get(id2,False)!=None
assert db.device.get(id3,False)==None

assert db.device.get(id1,True)!=None

id4=rd('id')+'0'
try:
    db.device.get(id4,True)
    assert False
except ValueError:
    pass

print('OK')
