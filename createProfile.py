import sys
import os.path
import json
import base64

class Profile:
  def __init__(self, title):
    self.id = 0
    self.title = title
    self.keepTitle = False
    self.icon = None
    self.note = ''
    self.roles = []
    self.topRole = ''

if len(sys.argv) != 4:
	print('Usage: python createProfile.py credits.json name role1,role2')
	sys.exit()
json_filename = sys.argv[1]
profile_name = sys.argv[2]
profile_roles = sys.argv[3].split(',')

new_profile = Profile(profile_name)
new_profile.roles = profile_roles
if os.path.isfile(profile_name + '.png'):
	profile_png = profile_name + '.png'
else:
	profile_png = 'default.png'
with open(profile_png, 'rb') as p:
	png_bytes = p.read()
	new_profile.icon = 'data:image/png;base64,{}'.format(base64.b64encode(png_bytes).decode('utf-8'))

with open(json_filename, 'r') as f:
	credits_json = json.load(f)
profiles = credits_json['profiles']
profiles.append(new_profile.__dict__)
credits_json['profiles'] = profiles
with open(json_filename, 'w') as f:
	json.dump(credits_json, f, indent=2)
print(f'Added new profile for {profile_name} to {json_filename}')