if [ $# -lt 1 ] ; then
    str='db_tmp'
else
    str=$1
fi
./before.sh $str
sudo -u $str python3 ./moduletest/admintest.py
sudo -u $str python3 ./moduletest/devicetest.py
sudo -u $str python3 ./moduletest/modeltest.py
./after.sh $str