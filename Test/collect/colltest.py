from distutils.cmd import Command
from gc import collect
import sys
import shlex
import subprocess

COUNT=64

command='sudo -u db python3 "%s"'%sys.argv[1]
print(command)
command=shlex.split(command)

for _ in range(COUNT):
    if not _&7:
        print('colltest',_)
    s=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out=s.stdout.read()
    err=s.stderr.read()
    if err:
        print(err.decode('utf8'))
        print('ERROR')
        sys.exit(1)
    else:
        l=[float(i) for i in out.decode('utf8').split(',')]
        assert len(l)==90

print('OK')
