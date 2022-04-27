useradd db
rm -r /home/db/data
mkdir -p /home/db/data
echo base_model > /home/db/data/base.mdl
chown -R db /home/db

sudo -u db python3 admin_add.py
sudo -u db python3 admin_check.py
sudo -u db python3 admin_remove.py
sudo -u db python3 device_banned.py
sudo -u db python3 device_calibration.py
sudo -u db python3 device_email.py
sudo -u db python3 device_get.py
sudo -u db python3 device_model.py
sudo -u db python3 device_remove.py
sudo -u db python3 model_getBase.py
sudo -u db python3 model_setBase.py
rm -r ./__pycache__
