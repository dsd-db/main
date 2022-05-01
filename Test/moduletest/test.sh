if [ $# -lt 1 ] ; then
    str='db_tmp'
else
    str=$1
fi
../before.sh $str
sudo -u $str python3 admintest.py
sudo -u $str python3 devicetest.py
sudo -u $str python3 modeltest.py
../after.sh $str
