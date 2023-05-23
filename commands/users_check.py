import sqlite3
import os

from discord.ext import commands
from ruamel.yaml import YAML
from .discordcolor import DiscordColors
from .permissions import permissions
from .output import Output

# Environment parameters
colors = DiscordColors('')
perm = permissions('')
output = Output('')
DB = os.environ['SQL']
path = os.getenv("DIR_PATH")

# Opens config 
yaml = YAML()
with open(path+"Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

    
class users_checker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def user_check(user_name):
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (str(user_name),))
        result = cursor.fetchone()

        if result == None:
            return 'None'
        else:
            return 

    def user_info(user_name):
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (str(user_name),))
        result = cursor.fetchone()

        if result == None:
            return 'None'
        else:
            return result
        
def setup(client):
    client.add_cog(users_checker(client))
                   