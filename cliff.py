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
    logtime(message)

def logtime(message):
    print(f'{datetime.datetime.now()} {message.content}')

client.run(config['token'])
