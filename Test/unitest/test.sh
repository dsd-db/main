useradd db_tmp
sudo -u db_tmp rm -r ~/data
sudo -u db_tmp python3 admin_add.py
sudo -u db_tmp python3 admin_check.py
sudo -u db_tmp python3 admin_remove.py
sudo -u db_tmp python3 device_banned.py
sudo -u db_tmp python3 device_calibration.py
sudo -u db_tmp python3 device_email.py
sudo -u db_tmp python3 device_get.py
sudo -u db_tmp python3 device_id.py
sudo -u db_tmp python3 device_model.py
sudo -u db_tmp python3 device_remove.py
sudo -u db_tmp python3 model_getBase.py
sudo -u db_tmp python3 model_setBase.py
rm -r ./__pycache__
sudo -u db_tmp rm -r ~/tmp
userdel db_tmp
