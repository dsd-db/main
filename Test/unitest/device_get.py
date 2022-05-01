import os
from uuid import UUID

import db
from initializate import rd

id1=rd('id')
id2=rd('id')
id3=rd('id')
uuid1=UUID(id1,version=4)
uuid2=UUID(id2,version=4)
uuid3=UUID(id3,version=4)
assert id1!=id2 and id1!=id3 and id2!=id3
assert db.device.get(id1,False)==None
assert db.device.get(id2,False)==None
assert db.device.get(id3,False)==None

d1=db.device.get(id1,True)
assert uuid1.hex==d1.id.hex
assert str(uuid1)==str(d1.id)
assert d1.banned==False
assert d1.email==None
assert d1.model==None
assert d1.calibration==None

d2=db.device.get(id2,True)
assert uuid2.hex==d2.id.hex
assert str(uuid2)==str(d2.id)
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
