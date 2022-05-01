if [ `id -g` != '0' ]; then
    echo "You must be root to run this script."
    exit 1
fi
rm -r ./__pycache__
rm -r /home/$1
userdel $1
