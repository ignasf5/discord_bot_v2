from discord.ext import commands

class permissions(commands.Cog):
    def __init__(self, permissions):
        self.bot = permissions

        self.permissions = {
            '0' :       {'name': 'Master'},
            '1' :       {'name': 'Admin'},
            '2' :       {'name': 'Valorant'},
            '3' :       {'name': 'Channel'},
            '7' :       {'name': 'Bet'},
            '23' :      {'name': 'Valorant, Channel'},
            '27' :      {'name': 'Valorant, Bet'},
            '237' :     {'name': 'Valorant, Channel, Bet'}
        }

    def permission_one(self, permissions:str):
        if permissions in self.permissions:
            return self.permissions[permissions]
        else:
            return 'None'
        
    def permissions_list(self):
        return self.permissions

def setup(bot):
    bot.add_cog(permissions(bot))