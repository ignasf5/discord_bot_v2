from discord.ext import commands

class Agents(commands.Cog):
    def __init__(self, agents):
        self.bot = agents

        self.agents = {
            'Astra' :           {'name': 'x'},
            'Breach' :          {'name': 'x'},
            'Brimstone' :       {'name': 'x'},
            'Jett' :            {'name': 'x'},
            'Killjoy' :         {'name': 'x'},
            'Omen' :            {'name': 'x'},
            'Gekko' :           {'name': 'x'},
            'Pheonix' :         {'name': 'x'},
            'Harbor' :          {'name': 'x'},
            'Kayo' :            {'name': 'x'},
            'Neon' :            {'name': 'x'},
            'Raze' :            {'name': 'x'},
            'Sage' :            {'name': 'x'},
            'Skye' :            {'name': 'x'},
            'Sova' :            {'name': 'x'},
            'Yoru' :            {'name': 'x'},
            'Fade' :            {'name': 'x'},
            'Chamber' :         {'name': 'x'},
            'Reyna' :           {'name': 'x'}
        }

    def agents_list(self, agents:str):
        if agents in self.agents:
            return self.agents[agents]
        else:
            return 'None'
        
    def get_agents(self):
        return self.agents

def setup(bot):
    bot.add_cog(Agents(bot))
