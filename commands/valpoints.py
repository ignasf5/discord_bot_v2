from discord.ext import commands

class ValorantPoints(commands.Cog):
    def __init__(self, valpoints):
        self.bot = valpoints

        self.valpoints = {
            'r':   {'name': 'Radiant',  'level_points': '10000' },
            'h':   {'name': 'High',     'level_points': '7500'},
            'm':   {'name': 'Mid',      'level_points': '5000'},
            'l':   {'name': 'Low',      'level_points': '2500'},

        }

    def valpoints_list(self, valpoints:str):
        if valpoints in self.valpoints:
            return self.valpointss[valpoints]
        else:
            return 'no valpoints'
        
    def get_valpoints_list(self):
        return self.valpoints
    
    def return_val_rank(self, valvalpoints: int):
        levels = list(self.valpoints.keys())
        for level in levels:
            if valvalpoints >= int(self.valpoints[level]['level_points']):
                return level
        return level

    # def return_val_rank(self, valvalpoints: int):
    #     levels = ['r', 'h', 'm', 'l']
    #     for level in levels:
    #         if valvalpoints >= int(self.valpoints[level]['level_points']):
    #             return level
    #     return 'l'

def setup(bot):
    bot.add_cog(ValorantPoints(bot))
