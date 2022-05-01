import os
from uuid import UUID

import db
from initializate import rd

id1=rd('id')
id2=rd('id')
assert id1!=id2
uuid1=UUID(id1,version=4)
uuid2=UUID(id2,version=4)

d1=db.device.get(id1,True)
assert uuid1.hex==d1.id.hex
assert str(uuid1)==str(d1.id)

d2=db.device.get(id2,True)
assert uuid2.hex==d2.id.hex
assert str(uuid2)==str(d2.id)

try:
    d1.id=''
    assert False
except:
    pass

print('OK')
