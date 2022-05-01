import os

import db
from initializate import rd

id1=rd('id')
id2=rd('id')
assert id1!=id2

d1=db.device.get(id1,True)
assert d1.banned==False

d2=db.device.get(id2,True)
assert d2.banned==False

d1.banned=True
assert d1.banned==True
assert d2.banned==False

print('OK')
