import discord
import sqlite3
import os

from discord.ext import commands
from ruamel.yaml import YAML

from .discordcolor import DiscordColors
from .valranks import ValorantRanks
from .picture_location import picture
from .output import Output
from .admins_check import admin_check

#TODO enable logger

# Environment parameters
output = Output('')
colors = DiscordColors('')
valrank = ValorantRanks('')
pictures = picture('')
DB = os.environ['SQL']
path = os.getenv("DIR_PATH")
admins_check = admin_check('')

# Opens the config 
yaml = YAML()
with open(path+"Configs\config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

class user_reg(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["reg", "register", "registration"])
    async def user_reg(bot, ctx,*, name=None):

        def check(msg):
            return msg.author == ctx.author
        
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (str(ctx.author),))
        result = cursor.fetchone()

        if result is not None:
            return await ctx.send('{} {}'.format(output.output_list('reg_yes')['name'], ctx.author))

        # if result == None:
        #     await ctx.send(output.output_list('enter_rank')['name'])
        #     try:
        #         my_rank = await bot.client.wait_for('message',check=check,timeout=15.0)

        #         if my_rank.content in valrank.get_rank_list():
        #             pass
        #         else:
        #             file = discord.File(pictures.get_picture('failed.png'), filename="image.png")
        #             em = discord.Embed(title=output.output_list('failed')['name'], description="", color=colors.color('red'))
        #             em.set_thumbnail(url="attachment://image.png")
        #             em.add_field(name=output.output_list('no_rank')['name'], value='\u200b', inline=False)
        #             em.set_footer(text=output.output_list('check_ranks')['name'])
        #             return await ctx.send(embed=em,file=file)
        #     except :
        #         return await ctx.channel.send(output.output_list('no_respond')['name'])

        my_rank = config['starting_rank']
        val_pts = config['valorant_rank_points']
        bet_pts = config['bet_points']
        reg_user = ctx.author
        game_count = config['game_count']
        games_win = config['games_win']
        games_tied = config['games_tied']
        games_lost = config['games_lost']
        bet_count = config['bet_count']
        bet_win = config['bet_win']
        bet_lost = config['bet_lost']

        try: 
            content_insert = (str(reg_user),int(val_pts),int(bet_pts),
                              str(my_rank),
                            int(game_count),int(bet_count),int(games_win),
                            int(games_tied),int(games_lost),int(bet_win),
                            int(bet_lost),str('none'),str('none')
                            )
            cursor.execute(f"""INSERT INTO {config['user_table']} 
            (user_id, val_pts, bet_pts, rank, games, bets, games_win, games_tied, games_lost, bet_win, bet_lost, LAST_GAME, LAST_BET, REG_DATA, UP_DATA)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?, DateTime('now'), DateTime('now'))""",content_insert)

            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)
            return await ctx.channel.send(output.output_list('no_db')['name'])

        try:
            file = discord.File(pictures.get_picture('verify.gif'), filename="image.gif")
            em2 = discord.Embed(title=output.output_list('congrats')['name'], description="", color=colors.color('green'))
            em2.set_thumbnail(url="attachment://image.gif")
            em2.add_field(name=('{} {} Points'.format(output.output_list('reg')['name'], config['bet_points'])), value=reg_user, inline=False)
            return await ctx.send(embed=em2,file=file)
        except:
            return await ctx.channel.send(output.output_list('embed_issue')['name'])

class user_ghost_reg(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["rghost"])
    async def user_ghost_reg(bot, ctx,*, name=None):

        admin_permissions_check = admins_check.admin_check(str(ctx.author))
        admin_val_permissions_check = admins_check.check_master_admin_per(str(ctx.author))

        # Check admin permissions
        if admin_permissions_check and admin_val_permissions_check:

            pass
        else:
            return await ctx.send(output.output_list('no_permissions')['name'])

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['user_table']} WHERE user_id = ?", (str(name),))
        result = cursor.fetchone()

        if result is not None:
            return await ctx.send(('{} {}'.format(output.output_list('reg_yes')['name'], str(name))))

        my_rank = config['starting_rank']
        val_pts = config['valorant_rank_points']
        bet_pts = config['bet_points']
        reg_user = str(name)
        game_count = config['game_count']
        games_win = config['games_win']
        games_tied = config['games_tied']
        games_lost = config['games_lost']
        bet_count = config['bet_count']
        bet_win = config['bet_win']
        bet_lost = config['bet_lost']

        try: 
            content_insert = (str(reg_user),int(val_pts),int(bet_pts),
                              str(my_rank),
                            int(game_count),int(bet_count),int(games_win),
                            int(games_tied),int(games_lost),int(bet_win),
                            int(bet_lost),str('none'),str('none')
                            )
            cursor.execute(f"""INSERT INTO {config['user_table']} 
            (user_id, val_pts, bet_pts, rank, games, bets, games_win, games_tied, games_lost, bet_win, bet_lost, LAST_GAME, LAST_BET, REG_DATA, UP_DATA)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?, DateTime('now'), DateTime('now'))""",content_insert)

            connection.commit()
            cursor.close()
            connection.close()
        except:
            return await ctx.channel.send(output.output_list('no_db')['name'])

        try:
            file = discord.File(pictures.get_picture('verify.gif'), filename="image.gif")
            em2 = discord.Embed(title=output.output_list('congrats')['name'], description="", color=colors.color('green'))
            em2.set_thumbnail(url="attachment://image.gif")
            em2.add_field(name=('{} {} Points'.format(output.output_list('reg')['name'], config['bet_points'])), value=reg_user, inline=False)
            return await ctx.send(embed=em2,file=file)
        except Exception as e:
            print(e)
            return await ctx.channel.send(output.output_list('embed_issue')['name'])

def setup(client):
    client.add_cog(user_reg(client))
    client.add_cog(user_ghost_reg(client))
                   