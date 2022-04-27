import os
import sys
import random

from initializate import r,rd
import db

if len(sys.argv)==1:
    COUNT=1024
else:
    COUNT=int(sys.argv[1])

a=dict()

def f(username,password):
    try:
        db.admin.add(username,password)
    except ValueError:
        pass
    else:
        print(repr(username),repr(password))
        assert ValueError==None

def g(s,c=-1):
    l=len(s)
    if c==-1:
        if l<=1:
            return ''
        n=random.randint(0,l-1)
        return s[:n]+s[n+1:]
    else:
        if l<1:
            return c
        n=random.randint(0,l)
        return s[:n]+c+s[n:]

for _ in range(COUNT):
    if not _&255:
        print('db.admin',_)
    i=random.randint(0,3)
    if i==0 or i==1:
        j=random.randint(0,5)
        if j==0 or j==1:
            s=r()
            p=rd('id')
            a[s]=p
            assert db.admin.add(s,p)==True
        elif j==2:
            if not a:
                continue
            s=random.choice(list(a.keys()))
            p=rd('id')
            assert db.admin.add(s,p)==False
        else:
            k=random.randint(1,15)
            if k&3==0:
                s=r()
            elif k&3==1:
                s=''
            elif k&3==2:
                s=rd('id').replace('-','')
                while len(s)<40:
                    s+=s
            else:
                s=g(r(),random.choice('!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~ \n\t\r\v\f\a\b\0\1\2\3\4\5\6'))
            if k>>2==0:
                p=rd('id')
            elif k>>2==1:
                p=''
            elif k>>2==2:
                p=rd('id')
                while len(p)<40:
                    p+=p
            else:
                p=g(rd('id'),random.choice('\n\t\r\v\f\a\b\0\1\2\3\4\5\6'))
            f(s,p)
    elif i==2:
        j=random.randint(0,2)
        if j==0:
            if not a:
                continue
            s=random.choice(list(a.keys()))
            p=a[s]
            assert db.admin.check(s,p)==True
        elif j==1:
            if not a:
                continue
            s=random.choice(list(a.keys()))
            p=rd('id')
            assert db.admin.check(s,p)==False
        else:
            s=r()
            p=rd('id')
            assert db.admin.check(s,p)==False
    else:
        j=random.randint(0,1)
        if j==0:
            if not a:
                continue
            s=random.choice(list(a.keys()))
            del a[s]
            db.admin.remove(s)
        else:
            s=r()
            db.admin.remove(s)

print('OK')
