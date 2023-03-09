import discord, json, keep_alive, asyncio, random, os, sys, datetime, time, traceback
from discord.ext import commands
from datetime import datetime
now = datetime.now

with open('config.json') as f:
  config = json.load(f)
token = config.get('token')
prefix = config.get("prefix")
vanity_url = (config.get("vanity"))
role_id = (config.get("role_id"))

intents = discord.Intents().all()
vanity = commands.Bot(command_prefix=f'{prefix}', intents=intents)
vanity.remove_command('help')


@vanity.event
async def on_ready():
  await vanity.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.competing, name="github/vqea"))
  print(f"connected to {vanity.user}")


@vanity.event
async def on_presence_update(before: discord.Member, after: discord.Member):
  if before.status == discord.Status.offline or after.status == discord.Status.offline: return   
    try:     
      if before.activity is None and after.activity is not None:
          role = after.guild.get_role(role_id)
          if vanity_url in after.activity.name:
            await after.add_roles(role)

      elif before.activity is not None and after.activity is not None:
           role = after.guild.get_role(role_id) 
           if vanity_url in before.activity.name and (not vanity_url in after.activity.name):
            await after.remove_roles(role)
           elif not vanity_url in before.activity.name and vanity_url in after.activity.name:
            await after.add_roles(role)

      elif before.activity is not None and after.activity is None:
          role = after.guild.get_role(role_id)
          if vanity_url in before.activity.name:
            await after.remove_roles(role)
    except: 
      pass

keep_alive.keep_alive()
vanity.run(token)
