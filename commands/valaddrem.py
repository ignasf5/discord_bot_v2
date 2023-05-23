from discord.ext import commands

class ValorantAddRemPoints(commands.Cog):
    def __init__(self, valpoints):
        self.bot = valpoints

        self.valpoints = {
            'r': {'r': (+30, -15), 'h': (+25, -17), 'm': (+20, -19), 'l': (+15, -22)},
            'h': {'r': (+40, -15), 'h': (+30, -15), 'm': (+25, -17), 'l': (+20, -19)},
            'm': {'r': (+50, -12), 'h': (+40, -13), 'm': (+30, -15), 'l': (+25, -17)},
            'l': {'r': (+60, -10), 'h': (+50, -12), 'm': (+40, -13), 'l': (+30, -15)}
        }

    def valaddrem_points(self, valpoints:str):
        if valpoints in self.valpoints:
            return self.valpointss[valpoints]
        else:
            return 'no valpoints'
        
    def valaddrem_points_list(self):
        return self.valpoints
    
    def calculate_points(self ,team_a: str, team_b: str):

        if team_a in self.valpoints and team_b in self.valpoints[team_a]:
            points_team_a, points_team_b = self.valpoints[team_a][team_b]
            return points_team_a, points_team_b
        elif team_b in self.valpoints and team_a in self.valpoints[team_b]:
            points_team_b, points_team_a = self.valpoints[team_b][team_a]
            return points_team_a, points_team_b
        else:
            return None

        # if team_a in self.valpoints and team_b in self.valpoints[team_a]:
        #     points_team_a, points_team_b = self.valpoints[team_a][team_b]
        #     return points_team_a, points_team_b
        # else:
        #     return None
        # if team_a in self.valpoints and team_b in self.valpoints[team_a]:
        #     return self.valpoints[team_a][team_b]
        # else:
        #     return None

def setup(bot):
    bot.add_cog(ValorantAddRemPoints(bot))
