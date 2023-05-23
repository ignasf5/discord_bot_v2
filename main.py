
import logging
import os
import discord
import sqlite3
import pytz

from discord.ext import commands
from os import listdir
from discord.ext.commands import CommandInvokeError
from ruamel.yaml import YAML
from dotenv import load_dotenv
from datetime import datetime
from commands.create_tables import create_table

#TODO DB BACKUP
#TODO tests before run
#TODO bet
#TODO valgame (controller + logger + output + compress !w itteration)
#TODO re-work db for user acc + hash include
#TODO create !users !lastgame

# Loading env
load_dotenv()

# Environment parameters
DB = os.environ['SQL']
db = create_table(DB) #for create table
conn = sqlite3.connect(DB) #for execture into db
c = conn.cursor() #for execture into db
token = os.getenv("DISCORD_TOKEN") 
channel = os.getenv("CHANNEL_ID")
data_base = os.getenv("SQL")
owner_id = os.getenv("OWNER")
path = os.getenv("DIR_PATH")

# Opens the config 
yaml = YAML()
with open(path+"Configs\config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Command Prefix and removes discord default help
bot = commands.Bot(command_prefix=commands.when_mentioned_or(config['Prefix']), help_command=None, owner_id = owner_id, intents=discord.Intents.all())
bot.remove_command('help')

#join to discord
@bot.event
async def on_ready():
    bot.launch_time = datetime.utcnow() #bot uptime
    config_status = config['bot_status']
    config_activity = config['bot_activity']
    activity=discord.Activity(type=discord.ActivityType.watching, name=config_status)

    logging.info('Getting info from Config')
    print("Application starts.")
    print('------')
    print('Logged In:')
    print(f"Username: {bot.user.name}\nID: {bot.user.id}")
    print('------')
    print(f"Status: {config_status}\nActivity: {config_activity}")
    print('------')
    await bot.change_presence(status=config_activity,activity=activity)

#collect data of user status
@bot.event
async def on_member_update(before, after):
    logging.info(f"{before.name} status changed from {before.status} to {after.status}")
    if str(before.status) != 'offline' and str(after.status) == 'offline':
        last_online = datetime.utcnow()
        user_tz = pytz.timezone('Europe/Vilnius')
        last_online = last_online.replace(tzinfo=pytz.utc).astimezone(user_tz)
        try:
            c.execute(f"INSERT OR REPLACE INTO {config['last_online_table']} (user_id, user_name, last_online) VALUES (?, ?, ?)",
                        (before.id, str(before), last_online.isoformat()))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.info(e)
        return

# logger
FORMAT = '[%(asctime)s]:[%(levelname)s]: %(message)s'
logging.basicConfig(filename=path+'Logs/logs.txt', level=logging.INFO, format=FORMAT)
logging.debug('Started Logging')
logging.info('Connecting to Discord.')

# loading py scripts
logging.info("************* Loading *************")
for fn in listdir(path+"Commands"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn}")
        bot.load_extension(f"commands.{fn[:-3]}")
        logging.info(f"Loaded {fn}")

logging.info(f"Loading: Economy System")
# bot.load_extension(f"Systems.Economy")
logging.info(f"Loaded Economy System")
logging.info("************* Loading Finished *************")

# create tables
logging.info("************* Creating Tables *************")
db.connect()

logging.info(db.create_table_last_online(config['last_online_table']))
db.create_table_last_online(config['last_online_table'])

logging.info(db.create_table_admin(config['admin_table']))
db.create_table_admin(config['admin_table'])

logging.info(db.create_table_users(config['user_table']))
db.create_table_users(config['user_table'])

logging.info(db.create_table_acc(config['user_acc_table']))
db.create_table_acc(config['user_acc_table'])

logging.info(db.create_table_match_history(config['valorant_game_history_table']))
db.create_table_match_history(config['valorant_game_history_table'])

db.close()
logging.info("************* Creating Tables Finished *************")

bot.run(token)