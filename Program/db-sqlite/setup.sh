pip uninstall -y db
pip install --upgrade build
python3 -m build
ls -lah ./dist
pip install ./dist/db-2.0.1-py3-none-any.whl
rm -r ./db.egg-info ./dist
