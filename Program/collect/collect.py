import os
import time
DIR=os.path.abspath(os.path.dirname(__file__))
CSV=os.path.join(DIR,'1.csv')

data=open(CSV,'r').read().split('\n')
n=len(data)
i=0
while True:
    print(data[i],flush=True)
    i=(i+1)%n
    time.sleep(1/20)
