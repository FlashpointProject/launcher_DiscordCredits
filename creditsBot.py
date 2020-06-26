import base64
import json
from pathlib import Path
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')
token = ''
valid_users = []
uncredited = []
with open('token.txt', 'r') as f:
  token = f.read().replace('\n', '')
with open('users.txt', 'r') as f:
  valid_users = map(int, f.read().splitlines())
with open('uncreditedRoles.txt', 'r') as f:
  uncredited = f.read().splitlines()

class Role:
  def __init__(self, name, color, noCategory):
    self.name = name
    self.color = color
    self.noCategory = noCategory

class Profile:
  def __init__(self, title):
    self.id = 0
    self.title = title
    self.icon = None
    self.note = ''
    self.roles = []
    self.topRole = ''

@bot.command()
async def run(ctx):
  if ctx.author.id in valid_users:
    # Setup
    guild = ctx.guild
    profiles = []
    roles = []
    totalNew = 0
    totalUpd = 0
    print('Finding users for {}'.format(guild.name))

    # Load old credits
    creditsPath = Path("credits.json")
    if creditsPath.is_file():
      with open('credits.json', 'r') as f:
        rawOldCredits = json.load(f)
        for rawProfile in rawOldCredits['profiles']:
          profile = Profile(rawProfile['title'])
          profile.icon = rawProfile['icon']
          profile.roles = rawProfile['roles']
          if 'id' in rawProfile:
            profile.id = rawProfile['id']
          if 'note' in rawProfile:
            profile.note = rawProfile['note']
          if 'topRole' in rawProfile:
            profile.topRole = rawProfile['topRole']
          profiles.append(profile)
        for rawRole in rawOldCredits['roles']:
          role = Role(rawRole['name'], rawRole['color'], 'noCategory' in rawRole)
          roles.append(role)

    # Find all roles
    for r in guild.roles:
      if r.name not in uncredited:
        role = None
        roleIndex = None
        # Load existing role if possible
        try:
          roleIndex = next(i for i, x in enumerate(roles) if x.name == r.name)
        except Exception:
          pass
        if roleIndex is None:
          role = Role(r.name, '', False)
        else:
          role = roles[roleIndex]
        role.color = str(r.color)
        if roleIndex is None:
          roles.append(role)
        else:
          roles[roleIndex] = role
    for r in roles:
      print(r.__dict__)

    # Find all users
    await bot.request_offline_members(guild)
    for member in guild.members:
      # Filter out excluded roles
      memberRoles = list(filter(lambda r: r.name not in uncredited, member.roles))
      if len(memberRoles) > 0:
        # If roles remain, must be credited
        profile = None
        profileIndex = None
        # Load existing profile if possible
        # Check ID first
        try:
          profileIndex = next(i for i, x in enumerate(profiles) if x.id == member.id)
        except Exception:
          pass
        if profileIndex is None:
          try:
            profileIndex = next(i for i, x in enumerate(profiles) if x.id == 0 and x.title == member.display_name)
          except Exception:
            pass
        if profileIndex is None:
          profile = Profile(member.display_name)
          totalNew += 1
          print('New Profile {}'.format(profile.title))
        else:
          profile = profiles[profileIndex]
          totalUpd += 1
          print('Upd Profile {}'.format(profile.title))
        profile.id = member.id
        profile.title = member.display_name
        asset = member.avatar_url_as(format='png', size=64)
        profile.icon = 'data:image/png;base64,{}'.format(base64.b64encode(await asset.read()).decode('utf-8'))
        profile.roles = []
        for role in memberRoles[::-1]:
          profile.roles.append(role.name)
        # Push index to list
        if profileIndex is None:
          profiles.append(profile)
        else:
          profiles[profileIndex] = profile

    # Save to file
    rawFile = {}
    rawFile['roles'] = []
    rawFile['profiles'] = []
    for role in roles:
      rawFile['roles'].append(role.__dict__)
    for profile in profiles:
      rawFile['profiles'].append(profile.__dict__)
    with open('credits_new.json', 'w') as f:
      f.write(json.dumps(rawFile, indent=2))

    await ctx.send('Parsed {} New, {} Updated, {} Total Profiles for Credits'.format(totalNew, totalUpd, len(profiles)))

print('starting bot')
bot.run(token)