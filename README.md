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

# Commands
```
    # Show active tickets
    @<bot> list
    
    # Resolve an active ticket
    @<bot> resolve [ticket_id | ticket_name]
```

# Ticket system
The bot has a list of active tickets.
Each ticket has the following information:
    - a ticket ID
    - a ticket name
    - a list of responsible users
        (all repsonsible users must resolve for a ticket to be resolved.
         a ticket with no responsible users can be resolved by anyone.)
    - (optional) a location
    - a lodgement date
    - a due date