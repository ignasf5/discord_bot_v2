from discord.ext import commands

class ValorantRanks(commands.Cog):
    def __init__(self, rank):
        self.bot = rank

        self.ranks = {
            'i1':   {'name': 'Iron 1',      'level_points': '10'},
            'i2' :  {'name': 'Iron 2',      'level_points': '20'},
            'i3' :  {'name': 'Iron 3',      'level_points': '30'},
            'b1' :  {'name': 'Bronze 1',    'level_points': '50'},
            'b2' :  {'name': 'Bronze 2',    'level_points': '60'},
            'b3' :  {'name': 'Bronze 3',    'level_points': '70'},
            's1' :  {'name': 'Silver 1',    'level_points': '100'},
            's2' :  {'name': 'Silver 2',    'level_points': '120'},
            's3' :  {'name': 'Silver 3',    'level_points': '140'},
            'g1' :  {'name': 'Gold 1',      'level_points': '180'},
            'g2' :  {'name': 'Gold 2',      'level_points': '220'},
            'g3' :  {'name': 'Gold 3',      'level_points': '260'},
            'p1' :  {'name': 'Platinum 1',  'level_points': '300'},
            'p2' :  {'name': 'Platinum 2',  'level_points': '350'},
            'p3' :  {'name': 'Platinum 3',  'level_points': '400'},
            'd1' :  {'name': 'Diamond 1',   'level_points': '480'},
            'd2' :  {'name': 'Diamond 2',   'level_points': '520'},
            'd3' :  {'name': 'Diamond 3',   'level_points': '570'},
            'a1' :  {'name': 'Ascendant 1', 'level_points': '650'},
            'a2' :  {'name': 'Ascendant 2', 'level_points': '720'},
            'a3' :  {'name': 'Ascendant 3', 'level_points': '800'},
            'im1' : {'name': 'Immortal 1',  'level_points': '950'},
            'im2' : {'name': 'Immortal 2',  'level_points': '1200'},
            'im3' : {'name': 'Immortal 3',  'level_points': '1500'},
            'r' :   {'name': 'Radiant',     'level_points': '2000'}
        }

    def rank_list(self, rank:str):
        if rank in self.ranks:
            return self.ranks[rank]
        else:
            return 'no rank'
        
    def get_rank_list(self):
        return self.ranks
    
    def get_closest_rank(self, points):
        closest_rank = None
        closest_difference = float('inf')  # Initialize with a large value
        
        for rank_key, rank_info in self.ranks.items():
            rank_points = int(rank_info['level_points'])
            difference = abs(points - rank_points)
            
            if difference < closest_difference:
                closest_difference = difference
                closest_rank = rank_key
        
        if closest_rank is not None:
            return closest_rank
            # return self.ranks[closest_rank]
        else:
            return 'No rank found'

def setup(bot):
    bot.add_cog(ValorantRanks(bot))
