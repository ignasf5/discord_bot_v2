import discord
import sqlite3
import os

from discord.ext import commands
from ruamel.yaml import YAML
from .discordcolor import DiscordColors
from .valranks import ValorantRanks
from .permissions import permissions
from. valmaps import ValMaps

# Environment parameters
val_map = ValMaps('')
colors = DiscordColors('')
valrank = ValorantRanks('')
perm = permissions('')
DB = os.environ['SQL']
path = os.getenv("DIR_PATH")

# Opens config 
yaml = YAML()
with open(path+"Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# General Help
class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["h"])
    async def help(self, ctx, helptype=None):
        em = discord.Embed(title="Bot command list:", description="", color=colors.color('background'))
        em.add_field(name="`!reg`", value="User Registration.")
        em.add_field(name="`!uhelp`", value="Users Commands.")
        em.add_field(name="`!ahelp`", value="Admin Commands.")
        em.add_field(name="`!valorant`", value="Valorant Game.")
        em.add_field(name="`!db`", value="Account Storage.")
        em.add_field(name="`!bet`", value="Bet Game.")
        em.add_field(name="`!other`", value="Fun Stuff.")
        em.set_footer(text="Discord bot")
        return await ctx.send(embed=em)

# User Help
class uhelp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["userh", "hu", "uh"])
    async def uhelp(self, ctx, helptype=None):
        em = discord.Embed(title="User Commands:", description="", color=colors.color('background'))
        em.add_field(name="`!mystats`", value="Full Statistic.")
        em.add_field(name="`!myrank`", value="Current Rank.")
        # em.add_field(name="`!uprank`", value="Update Your Rank.")
        em.add_field(name="`!balance`", value="Current Points.")
        em.add_field(name="", value="")
        em.set_footer(text="Discord bot")
        return await ctx.send(embed=em)

# DataBase help
class db(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["database"])
    async def db(self, ctx, helptype=None):
        em = discord.Embed(title="DataBase commands :", description="", color=colors.color('background'))
        em.add_field(name="`!add`", value="Add Account.")
        em.add_field(name="`!list`", value="List Accounts.")
        em.add_field(name="`!acc`", value="Details of Account.")
        em.add_field(name="`!uname`", value="Update Name.")
        em.add_field(name="`!upw`", value="Update Password.")
        em.add_field(name="`!ugid`", value="Update Game Id.")
        em.add_field(name="`!urank`", value="Update Accounts Rank.")
        em.add_field(name="`!ranks`", value="List Ranks.")
        em.add_field(name="", value="")
        em.set_footer(text="Discord bot")
        return await ctx.send(embed=em)

# Valorant Help
class valorant(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["valo", "vlr"])
    async def valorant(self, ctx, helptype=None):
        em = discord.Embed(title="Valorant Commands:", description="", color=colors.color('background'))
        em.add_field(name="`!start`", value="Start Valorant Game.")
        em.add_field(name="`!stop`", value="Stop Valorant Game.")
        em.add_field(name="`!join`", value="Join Game.")
        em.add_field(name="`!remove`", value="Leave Game.")
        em.add_field(name="`!players`", value="List Players.")
        em.add_field(name="`!vote`", value="Vote for Map.")
        em.add_field(name="`!maps`", value="Maps list.")
        # em.add_field(name="`!maketeams`", value="Create teams.")
        em.add_field(name="`!winner`", value="Team Winner.")
        em.add_field(name="`!stats`", value="User Statistic.")
        em.add_field(name="`!agent`", value="1 Random agent.")
        em.add_field(name="`!random`", value="Get 1-5 random agents.")
        em.add_field(name="", value="")
        em.set_footer(text="Valorant")
        return await ctx.send(embed=em)

# Admins help
class ahelp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["adm", "ah"])
    async def ahelp(self, ctx, helptype=None):
        em = discord.Embed(title="Admin Commands:", description="", color=colors.color('background'))
        em.add_field(name="`!admins`", value="Check Admins.")
        em.add_field(name="`!gadd {user}`", value="Add Admin.")
        em.add_field(name="`!grem {user}`", value="Remove Admin.")
        em.add_field(name="`!gupdate {user}`", value="Update Admin Permissions.")
        em.add_field(name="`!permissions`", value="Admin Permissions.")
        em.add_field(name="`!cusers`", value="List Chan Users.")
        # em.add_field(name="`!ban {user}`", value="Ban user.")
        # em.add_field(name="`!unban {user#000}`", value="Unban user.")
        # em.add_field(name="`!kick {user}`", value="Kick user.")
        # em.add_field(name="`!create-channel`", value="Creates text channel.")
        # em.add_field(name="`!create-voice`", value="Creates voice channel.")
        # em.add_field(name="`!delete-channel`", value="Deletes channel.")
        em.add_field(name="", value="")
        return await ctx.send(embed=em)

# Other
class other(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ot", "o"])
    async def other(self, ctx, helptype=None):
        em = discord.Embed(title="Fun Commands:", description="", color=colors.color('background'))
        em.add_field(name="`!av {user}`", value="User Avatar.")
        em.add_field(name="`!youtube`", value="Search video.")
        em.add_field(name="`!translate`", value="Translates text.")
        em.add_field(name="`!lastonline`", value="Last Seen User.")
        em.add_field(name="`!textall`", value="DM all.")
        em.add_field(name="`!poke`", value="Poke person.")
        # em.add_field(name="`!rulete`", value="Roulette Game.")
        # em.add_field(name="`!ping`", value="Pong.")
        # em.add_field(name="`!uptime`", value="Uptime Status.")
        em.add_field(name="`!gpt`", value="Chat GPT.")
        em.add_field(name="", value="")
        # em.set_footer(text="Discord bot")
        return await ctx.send(embed=em)

# Ranks
class help_ranks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ranks"])
    async def get_rank(self, ctx, helptype=None):
        em = discord.Embed(title="Ranks:", description="", color=colors.color('yellow'))

        for key,value in valrank.get_rank_list().items():
            em.add_field(name=value['name'], value=key)

        await ctx.send(embed=em)
        return

# Ranks Points
class rank_points(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["rp", "rank_points"])
    async def get_rank_points(self, ctx, helptype=None):
        em = discord.Embed(title="Ranks:", description="", color=colors.color('yellow'))

        for key,value in valrank.get_rank_list().items():
            em.add_field(name=value['name'], value=value['level_points']+" pts")

        await ctx.send(embed=em)
        return
    
# Maps list
class maps_listener(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["maps"])
    async def maps_listener(self, ctx, helptype=None):
        em = discord.Embed(title="Map List:", description="", color=colors.color('green'))

        for key,value in val_map.get_maps().items():
            em.add_field(name=key, value='', inline=True)
        em.add_field(name="", value="")

        return await ctx.send(embed=em)

# Admin Permissions
class admin_permissions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["permissions", "per"])
    async def list_permissions(self, ctx, helptype=None):
        em = discord.Embed(title="Permissions:", description="", color=colors.color('yellow'))

        for key,value in perm.permissions_list().items():
            em.add_field(name=value['name'], value=key)
        em.add_field(name="", value="")

        await ctx.send(embed=em)
        return

# Admin list
class admin_list(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["admins"])
    async def admins_list(self, ctx, helptype=None):

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        select = f"SELECT * FROM {config['admin_table']}"
        valorant_admin = discord.Embed(title="Valorant admin list", description="",color=colors.color('electric'))
        bet_admin = discord.Embed(title="Bet admin list", description="",color=colors.color('electric'))

        for x in cursor.execute(select):
            admin = x[0]
            permissions = x[1]
            if permissions == 2 or permissions == 23 or permissions == 27 or permissions == 237:
                valorant_admin.add_field(name="", value=admin,inline=False)
            if permissions == 7 or permissions == 27 or permissions == 37 or permissions == 237:
                bet_admin.add_field(name="", value=admin,inline=False)
            else:
                pass

        cursor.close()
        connection.close()
        await ctx.send(embed=valorant_admin)
        await ctx.send(embed=bet_admin)
        return

def setup(client):
    client.add_cog(db(client))
    client.add_cog(help(client))
    client.add_cog(ahelp(client))
    client.add_cog(uhelp(client))
    client.add_cog(valorant(client))
    client.add_cog(other(client))
    client.add_cog(help_ranks(client))
    client.add_cog(rank_points(client))
    client.add_cog(admin_permissions(client))
    client.add_cog(admin_list(client))
    client.add_cog(maps_listener(client))
