import sqlite3
import os
import discord

from discord.ext import commands
from ruamel.yaml import YAML
from .output import Output
from .discordcolor import DiscordColors
from .valranks import ValorantRanks
from .picture_location import picture, picture_with_path

#TODO create info about user
#TODO enable logger
#TODO Create table if not exist

# Environment parameters
picture_path = picture_with_path('')
pictures = picture('')
valrank = ValorantRanks('')
output = Output('')
colors = DiscordColors('')
DB = os.environ['SQL']
path = os.getenv("DIR_PATH")

# Opens config 
yaml = YAML()
with open(path+"Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# find key in dictionary
def find_key(dict, key):
    if key in dict:
        return key
    else:
        return None
    
# game_win_proc = (games/games_w)
def proc(x,y):
    try: 
        return x / y * 100
    except ZeroDivisionError:
        return 0

class list_channel_users(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["cusers", "cu"])
    async def list_channel_users(bot, ctx):

            members = ctx.channel.members
            for member in members:
                await ctx.send(f"{member.name}#{member.discriminator}")# - {member.id}")

    @commands.command(aliases=["myname"])
    async def myname_return(bot, ctx):
            await ctx.send(f"{ctx.author.name}#{ctx.author.discriminator}")

    @commands.command(aliases=["name"])
    async def channel_user_name(self, ctx, *, username=None):
        if username is None:
            return await ctx.send(output.output_list('no_user_given')['name'])

        members = ctx.channel.members
        found_member = None

        for member in members:
            if str(member) == username:
                found_member = member
                break

        if found_member is not None:
            return await ctx.send(f"{found_member.name}#{found_member.discriminator}")
        else:
            try:
                member = await commands.MemberConverter().convert(ctx, username)
                return  await ctx.send(f"{member.name}#{member.discriminator}")
            except commands.MemberNotFound:
                return await ctx.send(output.output_list('no_user')['name'])
            
class command_user(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["user", "u"])
    async def command_user(bot, ctx,*,name=None):

        def check(msg):
            return msg.author == ctx.author
        
        if name is None:
            return await ctx.send(output.output_list('no_acc')['name'] +' - !user user_name')
        
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (name,))
        result = cursor.fetchone()

        if result == None:
            return await ctx.send('{} example: `!u {}`'.format(output.output_list('no_user')['name'], ctx.author))
        
        else:
            # points = result[1]
            # games = result[3]
            # games_w = result[5]
            # games_l = result[7]
            # bet_total = result[4]
            # bet_w = result[8]
            # bet_l = result[9]
            # reg = result[12]
            # last_game = result[10]
            # last_bet = result[11]

            embed = discord.Embed(title=output.output_list('user_info')['name'], colour=colors.color('magenta'))
            embed.add_field(name=output.output_list('user_member_id')['name'], value="123456789", inline=False)
            embed.add_field(name=output.output_list('user_status')['name'], value="online", inline=False)
            embed.add_field(name=output.output_list('user_created')['name'], value="2017-06-14 19:28:07", inline=False)
            return await ctx.send(embed=embed)

# class user_rank_update(commands.Cog):
#     def __init__(self, bot):
#         self.client = bot

#     @commands.command(aliases=["uprank"])
#     async def user_rank_update(bot, ctx):

#         def check(msg):
#             return msg.author == ctx.author
        
#         connection = sqlite3.connect(DB)
#         cursor = connection.cursor()
#         cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (str(ctx.author),))
#         result = cursor.fetchone()

#         if result is None:
#             return await ctx.send(output.output_list('no_reg')['name'])

#         if result is not None:
#             await ctx.send('Enter your new rank')
#             try:
#                 my_rank = await bot.client.wait_for('message',check=check,timeout=15.0)

#                 if my_rank.content in valrank.get_rank_list():
#                     pass
#                 else:
#                     em = discord.Embed(title=output.output_list('failed')['name'], description="", color=colors.color('red'))
#                     em.add_field(name=output.output_list('no_rank')['name'], value='\u200b', inline=False)
#                     em.set_footer(text=output.output_list('check_ranks')['name'])
#                     return await ctx.send(embed=em)
#             except:
#                 return await ctx.channel.send(output.output_list('no_respond')['name'])

#             new_rank = my_rank.content
#             cursor.execute(f"""Update {config['user_table']} SET rank = ?, UP_DATA = DateTime('now') where user_id = ?""", (str(new_rank), str(ctx.author)))
#             connection.commit()
#             cursor.close()
#             connection.close()

#             image_key = find_key(valrank.get_rank_list(), new_rank)+".png"
#             file = discord.File(picture_path.get_picture_path(str(image_key), 'ranks'), filename="image.png")
#             em = discord.Embed(title=output.output_list('congrats')['name'], description="", color=colors.color('green'))
#             em.set_thumbnail(url="attachment://image.png")
#             em.add_field(name=output.output_list('update_rank')['name'], value=valrank.rank_list(new_rank)['name'], inline=False)
#             return await ctx.send(embed=em,file=file)


class user_balance(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["balance"])
    async def user_balance(bot, ctx):

        def check(msg):
            return msg.author == ctx.author
        
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (str(ctx.author),))
        result = cursor.fetchone()

        if result is None:
            return await ctx.send(output.output_list('reg')['name'])
        
        else:
            cursor.execute(f"Select bet_pts FROM {config['user_table']} WHERE user_id = ?", (str(ctx.author),))
            result = cursor.fetchone()
            return await ctx.send('{} {} points'.format(output.output_list('balance')['name'], result[0]))

class user_myrank(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["myrank"])
    async def user_myrank(bot, ctx):

        def check(msg):
            return msg.author == ctx.author
        
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (str(ctx.author),))
        result = cursor.fetchone()

        if result is None:
            return await ctx.send(output.output_list('no_reg')['name'])
        
        else:
            cursor.execute(f"Select rank, UP_DATA, val_pts FROM {config['user_table']} WHERE user_id = ?", (str(ctx.author),))
            result = cursor.fetchone()

            image_key = find_key(valrank.get_rank_list(), result[0])+".png"
            file = discord.File(picture_path.get_picture_path(str(image_key), 'ranks'), filename="image.png")

            em = discord.Embed(title=output.output_list('my_rank')['name'], description="", color=colors.color('white'))
            em.set_thumbnail(url="attachment://image.png")
            em.add_field(name=output.output_list('current_rank')['name'], value=valrank.rank_list(result[0])['name'], inline=False)
            em.add_field(name=str(result[2])+" points", value='', inline=False)
            em.add_field(name=output.output_list('last_mod')['name'], value=result[1], inline=False)
            return await ctx.send(embed=em,file=file)

class my_user_stats(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["mystats"])
    async def my_user_stats(bot, ctx):

        def check(msg):
            return msg.author == ctx.author
        
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (str(ctx.author),))
        result = cursor.fetchone()

        if result is None:
            return await ctx.send(output.output_list('no_reg')['name'])
        
        else:
            val_pts = result[1]
            # rank = result[3]
            games = result[4]
            games_w = result[6]
            # games_l = result[8]
            bet_total = result[5]
            bet_w = result[9]
            # bet_l = result[10]
            reg = result[13]
            # last_game = result[11]
            # last_bet = result[12]

            em = discord.Embed(title=output.output_list('acc_info')['name'], description=ctx.author, color=colors.color('white'))
            em.set_thumbnail(url="https://cdn3.emoji.gg/emojis/9656-stats.png")
                
            games_w_proc = round((proc(games_w, games)))
            bet_w_proc = round((proc(bet_w,bet_total)))

            em.add_field(name='''Statisctics: 
                    `Games played:` '''+ str(games) +'''
                    `Game Won:` '''+ str(games_w) +''' ('''+ str(games_w_proc) +'''%)
                    `Bet played:` '''+ str(bet_total) +'''
                    `Bet Won:` '''+ str(bet_w) +''' ('''+ str(bet_w_proc) +'''%)
            ''',  value='', inline=False)
            em.add_field(name="RR: " + str(val_pts),  value='', inline=False)
            em.add_field(name=output.output_list('registered')['name'] + str(reg),  value='', inline=False)
            return await ctx.send(embed=em)
            

class user_status_1(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    #TODO fix issue with users with # and without

    @commands.command(aliases=["stats", "st"])
    async def user_status_1(bot, ctx, *, user_name=None):

        if user_name is None:
            return await ctx.send(output.output_list('no_acc')['name'] +" example: `!stats "+ str(ctx.author)+"`")
            
        member = discord.utils.get(ctx.guild.members, name=user_name)

        if member is None:
            return await ctx.send('{} {}'.format(user_name, output.output_list('no_user')['name']))

        if user_name:
            try:
                connection = sqlite3.connect(DB)
                cursor = connection.cursor()
                cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (str(member),))
                result = cursor.fetchone()
                if result is None:
                    return await ctx.send(output.output_list('no_reg_user')['name'])
                    
                        #TODO result def
                else:
                    val_pts = result[1]
                    rank = result[3]
                    games = result[4]
                    games_w = result[6]
                    # games_l = result[8]
                    bet_total = result[5]
                    bet_w = result[9]
                    # bet_l = result[10]
                    reg = result[13]
                    # last_game = result[11]
                    # last_bet = result[12]
            except:
                return

        try:
            connection = sqlite3.connect(DB)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {config['last_online_table']} WHERE user_name=?", (str(member),))

            row = cursor.fetchone()
            if row is not None:
                last_online_str = row[2]
                convert_time = str(last_online_str)[:19].replace('T', ' ')
            else:
                last_online_str = None
                convert_time = 'no info'

        except:
            return

        try:
            if member:
                if member.status == discord.Status.online:
                    status = output.output_list('status_online')['name']
                elif member.status == discord.Status.idle:
                    status = output.output_list('status_away')['name']
                elif member.status == discord.Status.dnd:
                    status = output.output_list('status_dnd')['name']
                else:
                    status = output.output_list('status_offline')['name']

                games_w_proc = round((proc(games_w, games)))
                bet_w_proc = round((proc(bet_w,bet_total)))
                image_key = find_key(valrank.get_rank_list(), rank)+".png"

                rank_name = valrank.rank_list(rank)['name']

                file = discord.File(picture_path.get_picture_path(str(image_key), 'ranks'), filename="image.png")
                embed = discord.Embed(title=member, colour=colors.color('greyple'))
                embed.set_thumbnail(url="attachment://image.png")
                embed.add_field(name="RR: " + str(val_pts),  value='', inline=False)
                embed.add_field(name='''Statisctics: 
                        `Rank:` '''+ str(rank_name) +'''
                        `Games played:` '''+ str(games) +'''
                        `Game Won:` '''+ str(games_w) +''' ('''+ str(games_w_proc) +'''%)
                        `Bet played:` '''+ str(bet_total) +'''
                        `Bet Won:` '''+ str(bet_w) +''' ('''+ str(bet_w_proc) +'''%)
                        ''',  value='', inline=False)
                embed.add_field(name="`Registered`: "+ str(reg),  value='', inline=False)
                embed.add_field(name="`Last online`: "+ str(convert_time),  value='', inline=False)
                embed.set_footer(text=status)
                return await ctx.send(embed=embed, file=file)
        except Exception as e:
            print(e)
            return

def setup(client):
    client.add_cog(list_channel_users(client))
    client.add_cog(command_user(client))
    # client.add_cog(user_rank_update(client))
    client.add_cog(user_balance(client)) 
    client.add_cog(user_myrank(client))
    client.add_cog(my_user_stats(client))
    client.add_cog(user_status_1(client))
                   