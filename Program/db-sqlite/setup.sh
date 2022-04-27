if [ `whoami` != "root" ]; then
    echo "You must be root to run this script."
    exit 1
fi
useradd db
rm -r /home/db/data
mkdir -p /home/db/data
echo base_model > /home/db/data/base.mdl
chown -R db /home/db

rm -r ./db.egg-info ./dist
pip uninstall -y db
python3 -m build
ls -lah ./dist
pip install ./dist/db-0.0.3-py3-none-any.whl
# rm -r ./db.egg-info ./dist
