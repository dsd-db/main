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
UUID(d1.id,version=4)
assert d1.banned==False
assert d1.email==None
assert d1.model==None
assert d1.calibration==None

d2=db.device.get(id2,True)
UUID(d2.id,version=4)
assert d2.banned==False
assert d2.email==None
assert d2.model==None
assert d2.calibration==None

assert d1!=d2
assert db.device.get(id3,False)==None

id4=rd('id')+'0'
try:
    db.device.get(id4,True)
except ValueError:
    pass
else:
    assert ValueError==None

print('OK')
