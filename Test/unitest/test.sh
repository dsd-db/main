if [ $# -lt 1 ] ; then
    str='db_tmp'
else
    str=$1
fi
../before.sh $str
sudo -u $str python3 admin_add.py
sudo -u $str python3 admin_check.py
sudo -u $str python3 admin_remove.py
sudo -u $str python3 device_banned.py
sudo -u $str python3 device_calibration.py
sudo -u $str python3 device_email.py
sudo -u $str python3 device_get.py
sudo -u $str python3 device_id.py
sudo -u $str python3 device_model.py
sudo -u $str python3 device_remove.py
sudo -u $str python3 model_getBase.py
sudo -u $str python3 model_setBase.py
../after.sh $str
