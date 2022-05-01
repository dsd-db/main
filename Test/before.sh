if [ `id -g` != '0' ]; then
    echo "You must be root to run this script."
    exit 1
fi
rm -r /home/$1
useradd $1
mkdir -p /home/$1
chown -R $1 /home/$1
