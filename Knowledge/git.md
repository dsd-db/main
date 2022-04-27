## Git

### Tutorial

https://www.runoob.com/w3cnote/git-five-minutes-tutorial.html

https://www.runoob.com/git/git-tutorial.html

### Example

#### ssh

```sh
ssh-keygen -b 4096 -t rsa -C "userelaina@pm.me"
```

```sh
ls ~/.ssh
```
You will see your private key `id_rsa` and your public key `id_rsa.pub`.

```sh
cat ~/.ssh/id_rsa.pub
```

You will get a string like this:
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCm6mENFBfggeRcKPEs127IwvMi
Z+Yy9Jvbz7UHXG8NAZ7tS/HWVmLkavo942BH3zNTm1grocpI+CmALE1uXkMKU9y1
GHq9yoYO5hjsvvPI404Dc02upRaMSKFGJKcA2PXdSlHqZuXHVKqu3H6J7GYBvcRC
bqU1XvQGuR4bBbedvBwnzZ4p7143Zv6vNY06LAOc3VzDG6O4h/mc1iusAAUc7QJi
T9G5Cz4tZnhMw7mrSfnLNk7JCDYh+vq2i3XnozDNOetFDKxazP7FeTwcSg73CMvx
24uD3JfX7FPnUccPeqgJXdY0lNFrnbJYivl6f6o83RAo7mFtDdEzey/riC4xcmuO
FrAEOT94wCgTrd9Ve8hl7Oqo5xI4PlTZ+XdlR3MsD8wnv2O3tXvGSz5T1xOlsea2
Zes4VFbMmA7CG0hhQxL1R3bdAsZh4T4vu+NA/hlMb6rf82gDpmgrNzTLME+/GQ4A
L7WQCb/qesKoiXq7MrwWBUc2rsalfSSRO/z/rtgMNFpWR/Btu7tvoXE5YAqJ9wQ8
kmzDD/biNAGro8FLLLaJKcdAmz891BU7HW76stwhOIQjN5btwavFtlJFtwqkScST
TL1Wb7/8+398wlA7BG5n/jOOiwt4Zyp3NLxMtKOI6ROGGFpr6/nVtUdVk/uD86eC
9lW9XVRH1+03u4S+mw== userelaina@pm.me
```
Copy it and paste it to https://liyu.utad.pt/-/profile/keys.

```sh
ssh -T git@liyu.utad.pt
```
Welcome to GitLab, @elaina!

#### git config

```sh
git config --global user.email "userelaina@pm.me"
git config --global user.name "Elaina"
```

#### git clone

```sh
git clone git@liyu.utad.pt:happy-family/main.git
```
If this is your first time linking, you may need to enter `yes`.

#### git push
```sh
cd main
git add .
git commit -am 'update README.md'
git push
```

