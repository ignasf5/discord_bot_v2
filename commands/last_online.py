import discord
import sqlite3
import os
import pytz
import logging

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta

from ruamel.yaml import YAML
from .picture_location import picture
from .discordcolor import DiscordColors
from .output import Output

# Environment parameters
load_dotenv()
DB = os.environ['SQL']
path = os.getenv('DIR_PATH')
bot = discord.Client()
pictures = picture('')
colors = DiscordColors('')
output = Output('')

# Opens config 
yaml = YAML()
with open(path+"Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

connect_db = sqlite3.connect(DB)
cursor = connect_db.cursor()

class lastonline(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.logger = logging.getLogger('LastOnline')
        self.logger.setLevel(logging.INFO)
        
        # Create a file handler
        handler = logging.FileHandler(path+'Logs/online_log.txt')
        handler.setLevel(logging.INFO)
        
        # Create a formatter
        formatter = logging.Formatter('[%(asctime)s]:[%(levelname)s]: %(message)s')
        handler.setFormatter(formatter)
        
        # Add the handler to the logger
        self.logger.addHandler(handler)


    @commands.command(aliases=["l"])
    async def lastonline(client, ctx, *, member: discord.Member = None):
        client.logger.info(f'Message from {ctx.author}: {ctx.message.content}')

        if not member:
            return await ctx.send("Please specify a member")

        if not ctx.guild.get_member(member.id):
            return await ctx.send("The specified member is not in this server")
        
        if member:
            try:
                if member.status == discord.Status.idle:
                    status = output.output_list('status_away')['name']
                    color = colors.color('yellow')
                    image = pictures.get_picture('idle.png')
                if member.status == discord.Status.dnd:
                    status = output.output_list('status_dnd')['name']
                    color = colors.color('red')
                    image = pictures.get_picture('dnd.png')
                if member.status == discord.Status.online:
                    status = output.output_list('status_online')['name']
                    color = colors.color('green')
                    image = pictures.get_picture('online.png')
                else:
                    cursor.execute(f"SELECT {config['last_online_table']} FROM {config['last_online_table']} WHERE user_id=?", (member.id,))
                    result = cursor.fetchone()

                    if result:
                        last_online_str = result[0]
                        last_online = str(last_online_str)[:19].replace('T', ' ')
                        status = output.output_list('status_offline')['name']
                        image = pictures.get_picture('offline.png')
                        file = discord.File(image, filename="image.png")
                        embed = discord.Embed(title=member, colour=discord.Colour(colors.color('lighter_grey')))
                        embed.set_thumbnail(url="attachment://image.png")
                        embed.add_field(name='''Status:''',  value='', inline=False)
                        embed.add_field(name='''Last time seen:''',  value=last_online, inline=False)
                        return await ctx.send(embed=embed, file=file)
                    
            except Exception as e:
                print(e)

            file = discord.File(image, filename="image.png")
            embed = discord.Embed(title=member, colour=discord.Colour(color))
            embed.set_thumbnail(url="attachment://image.png")
            embed.add_field(name='Status:',  value=status, inline=False)
            return await ctx.send(embed=embed, file=file)
        else:
            return await ctx.send(f"{member.name} has not been seen online")

def setup(client):
    client.add_cog(lastonline(client))
