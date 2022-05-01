import os
from uuid import UUID

import db
from initializate import rd

id1=rd('id')
id2=rd('id')
assert id1!=id2
uuid1=UUID(id1)
uuid2=UUID(id2)

d1=db.device.get(id1,True)
assert uuid1.hex==UUID(d1.id,version=4).hex

d2=db.device.get(id2,True)
assert uuid2.hex==UUID(d2.id,version=4).hex

try:
    d1.id=''
    assert False
except:
    pass

print('OK')
