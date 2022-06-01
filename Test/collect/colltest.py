import sys
import time
import shlex
import subprocess

COUNT=512

command='python3 "%s"'%sys.argv[1]
print(command)
command=shlex.split(command)
s=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

for _ in range(COUNT):
    out=s.stdout.readline().decode('utf8')
    # print(repr(out))
    # time.sleep(1/20)
    l=[float(i) for i in out.split(',')]
    assert len(l)==45
    if not _&31:
        print('SUCC','colltest',_)

print('OK')
