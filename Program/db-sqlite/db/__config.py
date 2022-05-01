import os

DIR='~/data/'
DIR=os.path.abspath(os.path.expanduser(DIR))

BASE='base.mdl'
BASE=os.path.join(DIR,BASE)

DEVICE='device'
DEVICE=os.path.join(DIR,DEVICE)

MODEL='device.mdl'
MODEL=os.path.join(DEVICE,'%s',MODEL)

CALIBRATION='calibration'
CALIBRATION=os.path.join(DEVICE,'%s',CALIBRATION)

DB_ADMIN='admin.db'
DB_ADMIN=os.path.join(DIR,DB_ADMIN)

DB_DEVICE='device.db'
DB_DEVICE=os.path.join(DIR,DB_DEVICE)

os.makedirs(DEVICE,exist_ok=True)
open(BASE,'w').close()

if __name__=='__main__':
    print(DIR)
    print(BASE)
    print(DEVICE)
    print(MODEL)
    print(CALIBRATION)
    print(DB_ADMIN)
    print(DB_DEVICE)
