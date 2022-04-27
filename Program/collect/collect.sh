pip install --upgrade -r requirements.txt
useradd db
mkdir -p /home/db/collect
cp ./1.xlsx /home/db/collect/
echo 0 > /home/db/collect/1.conf
chown -R db /home/db
