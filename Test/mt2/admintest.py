import os
import sys
import random

from initializate import rd
import db

if len(sys.argv)==1:
    COUNT=1024
else:
    COUNT=int(sys.argv[1])

a=dict()

for _ in range(COUNT):
    if not _&255:
        print('db.admin',_)
    i=random.randint(0,3)
    if i==0:
        i=random.randint(0,1)
        if i==0:
            s=rd('id')
            p=rd('id')
            a[s]=p
            assert db.admin.add(s,p)==True
        else:
            if not a:
                continue
            s=random.choice(list(a.keys()))
            p=rd('id')
            assert db.admin.add(s,p)==False
    elif i==1 or i==2:
        i=random.randint(0,2)
        if i==0:
            if not a:
                continue
            s=random.choice(list(a.keys()))
            p=a[s]
            assert db.admin.check(s,p)==True
        elif i==1:
            if not a:
                continue
            s=random.choice(list(a.keys()))
            p=rd('id')
            assert db.admin.check(s,p)==False
        else:
            s=rd('id')
            p=rd('id')
            assert db.admin.check(s,p)==False
    else:
        i=random.randint(0,1)
        if i==0:
            if not a:
                continue
            s=random.choice(list(a.keys()))
            del a[s]
            db.admin.remove(s)
        else:
            s=rd('id')
            db.admin.remove(s)

print('OK')
