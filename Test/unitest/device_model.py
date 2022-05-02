import os

import db
from initializate import rd

id1=rd('id')
id2=rd('id')
assert id1!=id2

d1=db.device.get(id1,True)
assert d1.model==None

d2=db.device.get(id2,True)
assert d2.model==None

m1=rd('mdl')
m2=rd('mdl')
m3=rd('mdl')
assert m1!=m2 and m1!=m3 and m2!=m3
assert os.path.exists(m1)
assert os.path.exists(m2)
assert os.path.exists(m3)

d1.model=m1
assert d2.model==None
assert os.path.exists(m1)
assert os.path.exists(m2)
assert os.path.exists(m3)

r_m1=d1.model
assert os.path.exists(r_m1)

d2.model=m2
assert os.path.exists(m1)
assert os.path.exists(m2)
assert os.path.exists(m3)

r_m2=d2.model
assert os.path.exists(r_m2)

d1.model=m3
assert os.path.exists(m1)
assert os.path.exists(m2)
assert os.path.exists(m3)

assert d1.model==r_m1

assert os.path.exists(r_m1)
assert os.path.exists(r_m2)

db.device.remove(id1)
assert not os.path.exists(r_m1)
assert os.path.exists(r_m2)

d2.model=None
assert d2.model==None
assert not os.path.exists(r_m2)

print('OK')
