import os
import shutil
import random
TMP='~/tmp'
TMP=os.path.abspath(os.path.expanduser(TMP))
if os.path.exists(TMP):
    shutil.rmtree(TMP)
os.makedirs(TMP)

def rd(x:str=None)->str:
    if x=='id' or x=='uuid':
        s=str(random.randint(0,1000000))
    elif x=='email' or x=='mail':
        s=str(random.randint(0,1000000))+'@gov.cn'
    elif x=='mdl' or x=='model':
        s=os.path.join(TMP,'%d.mdl'%random.randint(0,1000000))
        with open(s,'w') as f:
            f.write('model:%s\n'%s)
    else:
        s=os.path.join(TMP,'%d'%random.randint(0,1000000),'')
        os.makedirs(s)
        for i in range(1,7):
            with open(os.path.join(s,'%d.csv'%i),'w') as f:
                f.write('%s,%d\n'%(s,i))
    return s
