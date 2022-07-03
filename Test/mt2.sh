if [ $# -lt 1 ] ; then
    str='db_tmp'
else
    str=$1
fi
./before.sh $str
sudo -u $str python3 ./mt2/admintest.py
sudo -u $str python3 ./mt2/devicetest.py
./after.sh $str
