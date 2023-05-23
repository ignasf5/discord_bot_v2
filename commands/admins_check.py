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

    
class admin_check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def admin_check(bot, admin_name):
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (str(admin_name),))
        result = cursor.fetchone()
        connection.close()
        if result == None:
            return 
        else:
            return result
        
#TODO think how to check permissions in faster way

    def admin_check_val_per(bot, admin_name):

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (str(admin_name),))
        result = cursor.fetchone()
        connection.close()
        if result == None:
            return 
        if result[1] == 0 or result[1] == 1 or result[1] == 2 or result[1] == 23 or result[1] == 27 or result[1] == 237:
            return result
        else:
            return 
        
    def check_master_admin_per(bot, admin_name):

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (str(admin_name),))
        result = cursor.fetchone()
        connection.close()
        if result == None:
            return 
        if result[1] == 0 or result[1] == 1:
            return result
        else:
            return 

    def first_time_match(bot, admin_name):

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        try:
            # Execute a SELECT query to count the number of records in the table
            # For the first game to DB
            cursor.execute(f"SELECT COUNT(*) FROM {config['valorant_game_history_table']}")
            result = cursor.fetchone()
            if result[0] == 0:
                data = (str(admin_name), 'bo1', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na')
                try:
                    cursor.execute(f"""INSERT INTO {config['valorant_game_history_table']} (NO, DATA, ADMIN, SYSTEM, MAP, WINNER, A1,A2,A3,A4,A5 ,B1,B2,B3,B4,B5) 
                                    VALUES (0, DateTime('now'), ?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)
                    connection.commit()
                    cursor.close()
                    connection.close()
                except Exception as e:
                    print(e)
                return
            else:
                return result[0]
        except Exception as e:
            print(e)
        return

def setup(client):
    client.add_cog(admin_check(client))
                   