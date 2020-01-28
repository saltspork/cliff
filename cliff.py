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
    if commands[0] == 'list':
        # TODO list active tickets
        logtime('TODO List active tickets here')
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
    # TODO
    pass

client.run(config['token'])
