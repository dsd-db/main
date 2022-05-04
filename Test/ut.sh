if [ $# -lt 1 ] ; then
    str='db_tmp'
else
    str=$1
fi
./before.sh $str
sudo -u $str python3 ./unitest/admin_add.py
sudo -u $str python3 ./unitest/admin_check.py
sudo -u $str python3 ./unitest/admin_remove.py
sudo -u $str python3 ./unitest/device_banned.py
sudo -u $str python3 ./unitest/device_calibration.py
sudo -u $str python3 ./unitest/device_email.py
sudo -u $str python3 ./unitest/device_get.py
sudo -u $str python3 ./unitest/device_id.py
sudo -u $str python3 ./unitest/device_model.py
sudo -u $str python3 ./unitest/device_remove.py
sudo -u $str python3 ./unitest/model_getBase.py
sudo -u $str python3 ./unitest/model_setBase.py
./after.sh $str
