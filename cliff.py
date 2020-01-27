#!/usr/bin/env python3

import discord, json, datetime, collections

with open('config.json') as f:
    config = json.load(f, object_pairs_hook=collections.OrderedDict)

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
    elif commands[0] == 'resolve':
        ticket_mark_resolved(ticket_id=commands[1], user=message.author)
        await channel.send(f'Ticket {commands[1]} marked as resolved by {message.author.name}')
    elif commands[0] == 'create':
        ticket_create(ticket_name=commands[1], user=message.author)
        await channel.send(f'Ticket {commands[1]} created by {message.author.name}')
    else:
        await channel.send(f'unknown command `{commands[0]}`')

def logtime(message):
    print(f'{datetime.datetime.now()} {message}')

def ticket_mark_resolved(ticket_id, user):
    # TODO
    pass

def ticket_create(ticket_name, user):
    # TODO
    pass

client.run(config['token'])
