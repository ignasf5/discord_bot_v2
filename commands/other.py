import discord
import os
import sqlite3
import re
import random

from urllib import parse, request
from googletrans import Translator
from discord.ext import commands
from datetime import datetime, timedelta
from .discordcolor import DiscordColors
from .valranks import ValorantRanks
from .picture_location import picture, picture_with_path
from .output import Output
from .agents import Agents

#TODO enable logger

output = Output('')
agents = Agents('')
picture_path = picture_with_path('')
pictures = picture('')
colors = DiscordColors('')

class other_stuff(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["textall", "ta"])
    async def textall_DM(bot, ctx, *, args=None):
        if args is not None:
            members = ctx.guild.members
            for member in members:
                try:
                    await member.send(f"{ctx.author} says: {args}")
                except discord.errors.Forbidden:
                    print(f"not sent: {member.name}")
                except discord.errors.HTTPException:
                    print(f"not sent: {member.name}")
        else:
            return await ctx.send("```Insert message \nExample: !textall hello```")

    @commands.command(aliases=["tl", "Tl", "Translate", "translate"])
    async def translationx(bot, ctx, lang=None, *, thing=None):

        if lang == None or thing == None:
            return await ctx.send(output.output_list('translate_none')['name']+' Example: `!translate en sveiki as Petras`') 

        else:
            translator = Translator()
            translation = translator.translate(thing, dest=lang)
            return await ctx.send(translation.text)

    @commands.command(aliases=["yt", "Youtube", "youtube", "YT"])
    async def yout(bot, ctx, *, search=None):

        if search == None:
            return await ctx.send(output.output_list('youtube_none')['name']+' Example: `!youtube Funny Memes`') 

        query_string = parse.urlencode({'search_query': search})
        html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
        search_content= html_content.read().decode()
        search_results = re.findall(r'\/watch\?v=\w+', search_content)
        return await ctx.send('https://www.youtube.com' + search_results[0])

    @commands.command(aliases=["av", "avatar"])
    async def user_avatar(bot, ctx, *,  avamember : discord.Member=None):
        if avamember == None:
            return await ctx.send(output.output_list('no_user_given')['name']+". Example: !av "+ str(ctx.author)) 
        
        else:
            userAvatarUrl = avamember.avatar_url
            return await ctx.send(userAvatarUrl)
        
    @commands.command(aliases=["agent"])
    async def pick_agent(bot, ctx):

        random_agent = random.choice(list(agents.get_agents()))

        file = discord.File(picture_path.get_picture_path(random_agent+'.png', 'agents'), filename="image.png")
        em = discord.Embed(title='Random agent', description="", color=colors.color('brown'))
        em.set_thumbnail(url="attachment://image.png")
        em.add_field(name="`Go play with`", value=random_agent, inline=False)
        
        await ctx.send(embed=em, file=file)


    @commands.command(aliases=["r", "random"])
    async def random_agent_choice(bot, ctx, *, python_list=None):

        if python_list is None:
            return await ctx.send("No number provided!")
            
        if python_list.isdigit():
            python_list = int(python_list)
            if python_list > 0:
                if python_list < 6:
                    agents_list = list(agents.get_agents())
                    get_list = random.sample(agents_list, k=python_list)
                    numba = 0
                    em = discord.Embed(title='Random agents', description="", color=colors.color('dark_magenta'))

                    for x in get_list:
                        numba += 1
                        em.add_field(name="`Player "+str(numba)+"`" , value=x, inline=False)

                    file = discord.File(pictures.get_picture('vct.png'), filename="image.png")
                    em.set_thumbnail(url="attachment://image.png")
                    return await ctx.send(embed=em, file=file)
                
                else:
                    return await ctx.send('I can take 1-5 selection')
            else:
                return await ctx.send('Please take between 1-5 numbers of players')
        else:
            return await ctx.send('Please use numbers instead of letters')

    @commands.command(aliases=["ping"])
    async def ping_check(bot, ctx):
        return await ctx.send(f'Pong! {round(bot.client.latency * 1000)}ms')

    @commands.command(aliases=["poke"])
    async def poke_user(bot, ctx, user: discord.Member=None):
        username = ctx.message.author.mention
        if user is None:
            return await ctx.send("```Insert user \nExample: !poke user (or @user)```")
        return await user.send(content=f":wave: from - {username}")
    
    @commands.command(aliases=["uptime","bot_uptime"])
    async def get_bot_uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

def setup(client):
    client.add_cog(other_stuff(client))