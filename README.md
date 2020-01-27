```
# Make 'tha schema
sqlite3 db.db < schema.sql

# create a venv
python3 -m venv venvdir

# use the venv
source venvdir/bin/activate
# Weird Fishes/Arpeggi
#source venvdir/bin/activate.fish

# install deps
pip3 install wheel
pip3 install -r requirements.txt

# run the bot
./cliff.py
```
