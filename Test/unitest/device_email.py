import os

from initializate import rd
import db

id1=rd('id')
id2=rd('id')
assert id1!=id2

d1=db.device.get(id1,True)
assert d1.email==None

d2=db.device.get(id2,True)
assert d2.email==None

e1=rd('email')
e2=rd('email')
e3=rd('email')
assert e1!=e2 and e1!=e3 and e2!=e3

d1.email=e1
assert d1.email==e1
assert d2.email==None

d2.email=e2
assert d1.email==e1
assert d2.email==e2

d1.email=e3
assert d1.email==e3
assert d2.email==e2

print('OK')
