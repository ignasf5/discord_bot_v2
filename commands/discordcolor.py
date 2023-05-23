from discord.ext import commands

class DiscordColors(commands.Cog):
    def __init__(self, color):
        self.bot = color

        # Define color codes
        self.colors = {
            'default' : 0,
            'red': 0xe74c3c,
            'dark_red' : 0x992d22,
            'teal' : 0x1abc9c,
            'dark_teal' : 0x11806a,
            'green': 0x00FF00,
            'dark_green' : 0x1f8b4c,
            'blue': 0x0000FF,
            'dark_blue' : 0x206694,
            'purple': 0x6A0DAD,
            'dark_purple' : 0x71368a,
            'magenta' : 0xe91e63,
            'dark_magenta' : 0xad1457,
            'yellow': 0xFFFF00,
            'electric': 0x00ffee,
            'orange': 0xFFA500,
            'dark_orange' : 0xa84300,
            'gold' : 0xf1c40f,
            'dark_gold' : 0xc27c0e,
            'pink': 0xFFC0CB,
            'brown': 0x8B4513,
            'teal': 0x008080,
            'white': 0xFFFFFF,
            'black': 0x000000,
            'lighter_grey' : 0x95a5a6,
            'dark_grey' : 0x607d8b,
            'light_grey' : 0x979c9f,
            'darker_grey' : 0x546e7a,
            'blurple' : 0x7289da,
            'greyple' : 0x99aab5,
            'background': 0x2f3136
        }

    def color(self, color_name:str):
        if color_name in self.colors:
            return self.colors[color_name]
        else:
            return 'No color'

def setup(bot):
    bot.add_cog(DiscordColors(bot))