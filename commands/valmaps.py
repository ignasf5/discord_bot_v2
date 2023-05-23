from discord.ext import commands

class ValMaps(commands.Cog):
    def __init__(self, maps):
        self.bot = maps

        self.maps = {
            'Bind' :          {'name': 'x'},
            'Haven' :         {'name': 'x'},
            'Split' :         {'name': 'x'},
            'Ascent' :        {'name': 'x'},
            'Icebox' :        {'name': 'x'},
            'Breeze' :        {'name': 'x'},
            'Fracture' :      {'name': 'x'},
            'Pearl' :         {'name': 'x'},
            'Lotus' :         {'name': 'x'}
        }

    def maps_list(self, maps:str):
        if maps in self.maps:
            return self.maps[maps]
        else:
            return 'None'
        
    def get_maps(self):
        return self.maps

def setup(bot):
    bot.add_cog(ValMaps(bot))
