useradd db_tmp
sudo -u db_tmp python3 admintest.py
sudo -u db_tmp python3 devicetest.py
sudo -u db_tmp python3 modeltest.py
rm -r ./__pycache__
sudo -u db_tmp rm -r ~/tmp
