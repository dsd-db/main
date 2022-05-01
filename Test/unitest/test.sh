useradd qwq
sudo -u qwq rm -r ~/data
sudo -u qwq python3 admin_add.py
sudo -u qwq python3 admin_check.py
sudo -u qwq python3 admin_remove.py
sudo -u qwq python3 device_banned.py
sudo -u qwq python3 device_calibration.py
sudo -u qwq python3 device_email.py
sudo -u qwq python3 device_get.py
sudo -u qwq python3 device_model.py
sudo -u qwq python3 device_remove.py
sudo -u qwq python3 model_getBase.py
sudo -u qwq python3 model_setBase.py
rm -r ./__pycache__
