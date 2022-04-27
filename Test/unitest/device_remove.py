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

db.device.remove(id1)
assert db.device.get(id1)==None
assert db.device.get(id2)!=None
assert db.device.get(id3)==None

assert db.device.get(id1,True)!=None

print('OK')
