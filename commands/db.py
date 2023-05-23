import discord
import os
import sqlite3

from discord.ext import commands
from ruamel.yaml import YAML
from .discordcolor import DiscordColors
from .valranks import ValorantRanks
from .picture_location import picture
from .output import Output

# Environment parameters
output = Output('')
colors = DiscordColors('')
valrank = ValorantRanks('')
pictures = picture('')
DB = os.environ['SQL']
path = os.getenv("DIR_PATH")

# Opens config 
yaml = YAML()
with open(path+"Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

#TODO re-work system to store acc (create table for each user)
#TODO add hash for password
#TODO enable logger
#TODO Create table if not exist

class get_list(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["list"])
    async def get_list(bot, ctx):

        owner = str(ctx.author)

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_acc_table']} WHERE owner IS ?", (owner,))
        fetch_all = cursor.fetchall()
        
        em = discord.Embed(title=output.output_list('acc_info')['name'], description="", color=colors.color('electric'))

        try:
            for x in fetch_all:
                user = x[0]
                rank = x[3]
                id = x[2]
            
                em.add_field(name=" `User` "+ user, value=rank+'  '+id,inline=False)
            em.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)

            cursor.close()
            connection.close()
            return await ctx.author.send(embed=em)
            
        except IndexError:
            em = discord.Embed(title=output.output_list('warning')['name'], description="", color=colors.color('red'))
            em.add_field(name="`You dont have any account yet`", value='\u200b', inline=False)
            em.set_footer(text="Maybe you wanted to `!add` account?")
            return await ctx.author.send(embed=em)

class get_list_all(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["alist"])
    async def get_list_all(bot, ctx):

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()

        select = f"SELECT * FROM {config['user_acc_table']}"
        embed = discord.Embed(title="Account list", description="", color=colors.color('electric'))

        for raw in cursor.execute(select):
            x = raw[0]
            rank = raw[3]
            id = raw[2]
            embed.add_field(name=" `User` "+ x, value=rank+'  '+id,inline=False)
        embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)
        cursor.close()
        connection.close()
        return await ctx.author.send(embed=embed)

class user_add_db(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["add"])
    async def user_add_db(bot, ctx, *args):

        if len(args) != 1:
            await ctx.send(f"Add account: !add account_name")
        else:
            def check(msg):
                return msg.author == ctx.author

            connection = sqlite3.connect(DB)
            cursor = connection.cursor()
            cursor.execute(f"SELECT account FROM {config['user_acc_table']} WHERE account = ?", (args[0],))
            result = cursor.fetchone()

            if result == None:
                pass
            else:
                em = discord.Embed(title=output.output_list('warning')['name'], description="", color=colors.color('orange'))
                em.add_field(name=output.output_list('acc_use')['name']+ args[0], value='\u200b', inline=False)
                em.set_footer(text="Maybe you wanted to `!update` info?")
                return await ctx.author.send(embed=em)

            await ctx.author.send(f'Enter password for {args[0]}')

            try:
                pw_msg = await bot.client.wait_for('message',check=check,timeout=15.0)
                if len(pw_msg.content) > 20:
                    return await ctx.channel.send(f'Message is too large\nQuit') #FIX
            except:
                return await ctx.channel.send(output.output_list('no_respond')['name'])

            await ctx.author.send("Enter user id")

            try:
                id_msg = await bot.client.wait_for('message',check=check,timeout=15.0)
                if len(id_msg.content) > 25:
                    return await ctx.channel.send(f'Message is too large\n[maximum 25 symbols]') #FIX
            except:
                return await ctx.channel.send(output.output_list('no_respond')['name'])

            await ctx.author.send("Enter account rank")
            
            try:
                rank_msg = await bot.client.wait_for('message',check=check,timeout=15.0)
                if len(rank_msg.content) > 10:
                    return await ctx.channel.send(f'Message is too large\n[maximum 10 symbols]') #FIX
                # if rank_msg.content in ranks:
                if rank_msg.content in valrank.get_rank_list():
                    pass
                else:
                    em = discord.Embed(title=output.output_list('failed')['name'], description="", color=colors.color('red'))
                    em.add_field(name="`Rank doesn't exist`", value='\u200b', inline=False) #FIX
                    em.set_footer(text="check ranks - !ranks ") #FIX
                    return await ctx.author.send(embed=em)
            except:
                return await ctx.channel.send(output.output_list('no_respond')['name'])

        name = args[0]
        owner = ctx.author
        data = (name, pw_msg.content, id_msg.content, rank_msg.content, str(owner))

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        
        cursor.execute(f"""INSERT INTO {config['user_acc_table']}
        (ACCOUNT, PASSWORD, GAME_ID, RANK, OWNER, DATA) 
        VALUES(?,?,?,?,?, DateTime('now'))""",data)

        connection.commit()
        cursor.close()
        connection.close()

        em = discord.Embed(title=output.output_list('congrats')['name'], description="", color=colors.color('green'))
        em.add_field(name="`Successfully added account`", value=name, inline=False) #FIX
        return await ctx.author.send(embed=em)

class update_user_rank_db(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["urank"])
    async def update_user_rank_db(bot, ctx, name=None):

        def check(msg):
            return msg.author == ctx.author

        if name is None:
            return await ctx.send('No account name was given - !urank account_name') #FIX

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_acc_table']} WHERE account = ?", (name,))
        result = cursor.fetchone()

        if result == None:
            await ctx.send(f"Account '{name}' not found") #FIX
            
        if str(result[4]) == str(ctx.author):
            await ctx.author.send(f'Enter new rank for {name}') #FIX
            try:
                new_rank = await bot.client.wait_for('message',check=check,timeout=15.0)

                if new_rank.content in valrank.get_rank_list():
                    pass
                else:
                    file = discord.File(pictures.get_picture('failed.png'), filename="image.png")
                    em = discord.Embed(title=output.output_list('failed')['name'], description="", color=colors.color('red'))
                    em.set_thumbnail(url="attachment://image.png")
                    em.add_field(name="`Rank doesn't exist`", value='\u200b', inline=False) #FIX
                    em.set_footer(text="check ranks - !ranks ") #FIX
                    return await ctx.author.send(embed=em,file=file)

            except Exception as e:
                print(e)
                return await ctx.channel.send(f'Sorry, you took too long to respond') #FIX

            x = new_rank.content
            cursor.execute(f"""Update {config['user_acc_table']} SET RANK = ?, DATA = DateTime('now') where ACCOUNT = ?""", (str(x), str(name)))
            connection.commit()
            cursor.close()
            connection.close()

            file = discord.File(pictures.get_picture('accepted.png'), filename="image.png")
            em = discord.Embed(title=output.output_list('congrats')['name'], description="", color=colors.color('green'))
            em.set_thumbnail(url="attachment://image.png")
            em.add_field(name="`Successfully updated rank:` "+x, value=name, inline=False) #FIX
            return await ctx.author.send(embed=em,file=file)

        else:
            await ctx.send('You dont have permissions') #FIX
        return

class list_user_info_acc(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["acc"])
    async def list_user_info_acc(bot, ctx, name=None):
        
        if name is None:
            await ctx.send(output.output_list('no_acc')['name'] +' - !acc account_name')
            return

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_acc_table']} WHERE account = ?", (name,))
        result = cursor.fetchone()

        if result == None:
            await ctx.send('{} {}'.format(name, output.output_list('no_user')['name']))
            
#TODO rework + new system for DB

        if str(result[4]) == str(ctx.author):

            iron = discord.File("C:/Users/InI/OneDrive/Desktop/dc/images/test/iron3.png", filename="image.png")
            bronze = discord.File("C:/Users/InI/OneDrive/Desktop/dc/images/test/bronze.png", filename="image.png")
            silver = discord.File("C:/Users/InI/OneDrive/Desktop/dc/images/test/silver.png", filename="image.png")
            gold = discord.File("C:/Users/InI/OneDrive/Desktop/dc/images/test/gold.png", filename="image.png")
            platinum = discord.File("C:/Users/InI/OneDrive/Desktop/dc/images/test/platinum.png", filename="image.png")
            diamond = discord.File("C:/Users/InI/OneDrive/Desktop/dc/images/test/diamond.png", filename="image.png")
            ascendant = discord.File("C:/Users/InI/OneDrive/Desktop/dc/images/test/ascendant.png", filename="image.png")
            immortal = discord.File("C:/Users/InI/OneDrive/Desktop/dc/images/test/immortal.png", filename="image.png")
            radiant = discord.File("C:/Users/InI/OneDrive/Desktop/dc/images/test/radiant.png", filename="image.png")
            
            em = discord.Embed(title=output.output_list('acc_info')['name'], description="", color=colors.color('white'))
            em.set_thumbnail(url="attachment://image.png")
            em.add_field(name="`User`: "+ result[0],  value='\u200b', inline=False)
            em.add_field(name="`Password`: "+ result[1], value='\u200b', inline=False)
            em.add_field(name="`Game ID`: "+ result[2], value='\u200b', inline=False)
            em.add_field(name="`Rank`: "+ result[3], value='\u200b', inline=False)
            em.set_footer(text="Updated: "+ result[5])
            if result[3] == "i1" or result[3] == "i2" or result[3] == "i3":
                await ctx.author.send(file=iron,embed=em)
            elif result[3] == "b1" or result[3] == "b2" or result[3] == "b3":
                await ctx.author.send(file=bronze,embed=em)
            elif result[3] == "s1" or result[3] == "s2" or result[3] == "s3":
                await ctx.author.send(file=silver,embed=em)
            elif result[3] == "g1" or result[3] == "g2" or result[3] == "g3":
                await ctx.author.send(file=gold,embed=em)
            elif result[3] == "p1" or result[3] == "p2" or result[3] == "p3":
                await ctx.author.send(file=platinum,embed=em)
            elif result[3] == "d1" or result[3] == "d2" or result[3] == "d3":
                await ctx.author.send(file=diamond,embed=em)
            elif result[3] == "a1" or result[3] == "a2" or result[3] == "a3":
                await ctx.author.send(file=ascendant,embed=em)
            elif result[3] == "im1" or result[3] == "im2" or result[3] == "im3":
                await ctx.author.send(file=immortal,embed=em)
            elif result[3] == "r":
                await ctx.author.send(file=radiant,embed=em)
            else:
                await ctx.author.send(embed=em)

            cursor.close()
            connection.close()
        else:
            await ctx.send(output.output_list('permissions')['name'])
        return

def setup(client):
    client.add_cog(get_list(client))
    client.add_cog(get_list_all(client))
    client.add_cog(user_add_db(client))
    client.add_cog(update_user_rank_db(client))
    client.add_cog(list_user_info_acc(client))
                   