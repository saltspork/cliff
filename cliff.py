#!/usr/bin/env python3

import discord, json, datetime, collections, sqlite3

with open('config.json') as f:
    config = json.load(f, object_pairs_hook=collections.OrderedDict)

con = sqlite3.connect('db.db')

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if client.user not in message.mentions:
        return

    logtime(f'Mentioned in: {message.content}')
    channel = message.channel

    # Parse message as a command
    commands = message.content.split()[1:]

    if commands[0] == 'help':
        await channel.send(
            '_\n**available commands** (options wrapped in `[]`)\n'
            + f'\t`@{client.user.name} list [all]`: list all active tickets (inactive also if `all`)\n'
            + f'\t`@{client.user.name} create <ticket-name>`: create a new ticket\n'
            + f'\t`@{client.user.name} resolve <ticket-name>`: resolve an active ticket'
        )
    elif commands[0] == 'list':
        await tickets_show(message.guild, channel,
                           only_active=(not (len(commands) > 1 and commands[1] == 'all')))
    elif commands[0] == 'create':
        ticket_create(guild=message.guild, user=message.author, ticket_name=commands[1])
        await channel.send(f'Ticket {commands[1]} created by {message.author.name}')
    elif commands[0] == 'resolve':
        ticket_mark_resolved(guild=message.guild, user=message.author, ticket_name=commands[1])
        await channel.send(f'Ticket {commands[1]} marked as resolved by {message.author.name}')
    else:
        await channel.send(f'unknown command `{commands[0]}`')

def logtime(message):
    print(f'{datetime.datetime.now()} {message}')

def pad_to_size(s, n):
    s = str(s)
    return f'{s}{" " * max(0, n - len(s))}'

async def tickets_show(guild, channel, only_active=True):
    query = (
        f'SELECT * FROM tickets WHERE guild_id = {guild.id}'
        + (' AND active = 1' if only_active else '')
    )
    cur = con.cursor()

    def fmt_row(row):
        guild_id, ticket_name, active, author, location, datetime_created = row

        if location is None:
            location = '' 

        # If datetime_created is an ISO 8601 string, try shortening it.
        try:
            dt = datetime.datetime.strptime(datetime_created, '%Y-%m-%d %H:%M:%S.%f')
            dt = dt.strftime('%a %d/%m')
        except ValueError:
            # If that fails, just take the date-time as a string.
            dt = str(datetime_created)
        return (
              '|' + pad_to_size(dt, 12)
            + '|' + pad_to_size(ticket_name, 12)
            + ('|' + pad_to_size(active, 7) if not only_active else '')
            + '|' + pad_to_size(author, 11)
            + '|' + pad_to_size(location, 10)
            + '|'
        )

    table = (
        '```'
        + fmt_row(("Guild", "Ticket Name", "Active", "Creator", "Location", "Created at")) + '\n'
        + '\n'.join([fmt_row(row) for row in cur.execute(query)])
        + '```'
    )

    await channel.send(table)
    con.commit()

def ticket_create(guild, user, ticket_name, location=None):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)",
        (guild.id,
         ticket_name,
         1,
         user.name,
         location,
         str(datetime.datetime.now()),
        )
    )
    con.commit()

def ticket_mark_resolved(guild, user, ticket_name):
    cur = con.cursor()
    cur.execute(
        "UPDATE tickets SET active = 0 "
        + f"WHERE guild_id = {guild.id} AND ticket_name = '{ticket_name}'"
    )
    con.commit()

client.run(config['token'])
