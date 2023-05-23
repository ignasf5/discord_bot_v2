import sqlite3
import discord
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

#TODO FIX: each admin with 0/1 permissions can remove everything
#TODO Maybe admin commands only can see admins?
#TODO enable logger
#TODO Create admin table if not exist

class admin_add(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["gadd"])
    async def add_admin(bot, ctx, *, name=None):

        def check(msg):
            return msg.author == ctx.author

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (str(ctx.author),))
        result = cursor.fetchone()
        if result == None:
            return await ctx.send(output.output_list('no_permissions')['name'])

        if name is None:
            return await ctx.send(output.output_list('no_acc')['name'] +' !gadd account_name')
            
        if result[0] == str(ctx.author) and result[1] == 1 or result[1] == 0:
            members = ctx.channel.members
            users_list = [member.name+"#"+member.discriminator for member in members]

        if name not in users_list:
            return await ctx.send('{} - {}'.format(name, output.output_list('no_user')['name']))
        
        cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (str(name),))
        result_check = cursor.fetchone()
        if result_check == None:
            pass
        else:
            return await ctx.send(f"Account '{name}' already have permissions")
            
        await ctx.author.send(output.output_list('check_perm')['name'])
        await ctx.author.send(f'`Enter permissions for {name}`')

        try:
            add_permissions = await bot.client.wait_for('message',check=check,timeout=15.0)

            if add_permissions.content in perm.permissions_list():
                pass
            else:
                em = discord.Embed(title=output.output_list('failed')['name'], description="", color=colors.color('red'))
                em.add_field(name="`Permissions doesn't exist`", value='\u200b', inline=False)
                em.set_footer(text=(output.output_list('check_perm')['name']))
                return await ctx.author.send(embed=em)
        except:
            return await ctx.author.send(output.output_list('no_respond')['name'])
        
        x = add_permissions.content
        content_insert = (str(name),str(x),str(ctx.author))
        cursor.execute(f"""INSERT INTO {config['admin_table']} 
        (Admin_name, Permissions, Last_mod, DATA)
        VALUES(?,?,?, DateTime('now'))""",content_insert)
        connection.commit()
        cursor.close()
        connection.close()

        em = discord.Embed(title=output.output_list('congrats')['name'], description="", color=colors.color('green'))
        em.add_field(name="`Successfully added permissions :` "+x, value='', inline=False)
        em.add_field(name=perm.permission_one(x)['name'], value='Admin', inline=False)
        msg_format = ('{} {}').format(output.output_list('new_perm')['name'], name)
        em.set_footer(text=msg_format)
        return await ctx.author.send(embed=em)
    
class admin_update(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["gupdate"])
    async def admin_update(bot, ctx,*, name=None):

        def check(msg):
            return msg.author == ctx.author

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (str(ctx.author),))
        result = cursor.fetchone()
        if result == None:
            return await ctx.send(output.output_list('no_permissions')['name'])

        if name is None:
            return await ctx.send(output.output_list('no_acc')['name'] +' !gupdate account_name')

        if result[0] == str(ctx.author) and result[1] == 1 or result[1] == 0:
            cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (name,))
            result = cursor.fetchone()

            if result == None:
                return await ctx.send(ctx.send('{} - {}'.format(name, output.output_list('no_user')['name'])))

            if result[1]:
                em = discord.Embed(title=output.output_list('curent_per')['name'], description="", color=colors.color('yellow'))
                format_msg = ('{} ({})'.format(str(result[1]), perm.permission_one(str(result[1]))['name']))
                em.add_field(name=format_msg, value='', inline=False)
                em.add_field(name='', value='', inline=False)
                em.add_field(name='', value='', inline=False)
                em.add_field(name=f'`Enter New Permissions For {name}`', value='', inline=False)
                em.set_footer(text=output.output_list('check_perm')['name'])

            await ctx.author.send(embed=em)

            try:
                update_permissions = await bot.client.wait_for('message',check=check,timeout=15.0)

                if update_permissions.content in perm.permissions_list():
                    pass
                else:
                    em = discord.Embed(title=output.output_list('failed')['name'], description="", color=colors.color('red'))
                    em.add_field(name="`Permissions doesn't exist`", value='\u200b', inline=False)
                    em.set_footer(text=(output.output_list('check_perm')['name']))
                    return await ctx.author.send(embed=em)
            except:
                return await ctx.author.send(output.output.output_list('no_respond')['name'])

            x = update_permissions.content
            cursor.execute(f"""Update {config['admin_table']} SET PERMISSIONS = ?, DATA = DateTime('now'), LAST_MOD = ? where Admin_name = ?""", (str(x),str(ctx.author) ,str(result[0])))
            connection.commit()
            cursor.close()
            connection.close()

            em = discord.Embed(title=output.output_list('congrats')['name'], description="", color=colors.color('green'))
            em.add_field(name="`Successfully updated permissions:` "+x, value='', inline=False)
            em.add_field(name=perm.permission_one(x)['name'], value='Admin', inline=False)
            msg_format = ('{} {}').format(output.output_list('new_perm')['name'], name)
            em.set_footer(text=msg_format)
            return await ctx.author.send(embed=em)

        else:
            await ctx.send(output.output_list('no_permissions')['name'])
        return


class admin_remove(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(aliases=["grem"])
    async def remove_admin(bot, ctx,*, name=None):

        def check(msg):
            return msg.author == ctx.author

        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (str(ctx.author),))
        result = cursor.fetchone()
        if result == None:
            return await ctx.send(output.output_list('no_permissions')['name'])
            
        if name is None:
            return await ctx.send(output.output_list('no_acc')['name'] +' !grem account_name')

        if result[0] == str(ctx.author) and result[1] == 1 or result[1] == 0:
            cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (str(name),))
            results = cursor.fetchone()
            if results is None:
                await ctx.send(f"User '{name}' is not admin") 
            if name in results[0]:
                    cursor.execute(f"DELETE FROM {config['admin_table']} WHERE Admin_name = ?", (str(name),))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    em = discord.Embed(title=output.output_list('congrats')['name'], description="", color=colors.color('green'))
                    em.add_field(name="`Successfully removed permissions`", value=name, inline=False)
                    return await ctx.send(embed=em)
        else:
            return await ctx.author.send(output.output_list('no_permissions')['name'])

def setup(client):
    client.add_cog(admin_add(client))
    client.add_cog(admin_update(client))
    client.add_cog(admin_remove(client))
                   