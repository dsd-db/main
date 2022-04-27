useradd db
rm -r /home/db/data
mkdir -p /home/db/data
echo base_model > /home/db/data/base.mdl
chown -R db /home/db

sudo -u db python3 admintest.py
sudo -u db python3 devicetest.py
sudo -u db python3 modeltest.py
rm -r ./__pycache__
