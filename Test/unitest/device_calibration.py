import os

from initializate import rd
import db

id1=rd('id')
id2=rd('id')
assert id1!=id2

d1=db.device.get(id1,True)
assert d1.calibration==None

d2=db.device.get(id2,True)
assert d2.calibration==None

c1=rd('c')
c2=rd('c')
c3=rd('c')
assert c1!=c2 and c1!=c3 and c2!=c3
assert os.listdir(c1)
assert os.listdir(c2)
assert os.listdir(c3)

d1.calibration=c1
assert d2.calibration==None
assert not os.path.exists(c1)
assert os.listdir(c2)
assert os.listdir(c3)

r_c1=d1.calibration
assert os.listdir(r_c1)

d2.calibration=c2
assert not os.path.exists(c1)
assert not os.path.exists(c2)
assert os.listdir(c3)

r_c2=d2.calibration
assert os.listdir(r_c2)

d1.calibration=c3
assert not os.path.exists(c1)
assert not os.path.exists(c2)
assert not os.path.exists(c3)

assert d1.calibration==r_c1

assert os.listdir(r_c1)
assert os.listdir(r_c2)

db.device.remove(id1)
assert not os.path.exists(r_c1)
assert os.listdir(r_c2)

print('OK')
