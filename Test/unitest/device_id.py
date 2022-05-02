import os
from uuid import UUID

import db
from initializate import rd

id1=rd('id')
id2=rd('id')
assert id1!=id2

d1=db.device.get(id1,True)
assert id1==d1.id.hex

d2=db.device.get(id2,True)
assert id2==d2.id.hex

try:
    d1.id=''
    assert False
except:
    pass

print('OK')
