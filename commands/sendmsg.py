from discord.ext import commands

class SendingMsg(commands.Cog):
    def __init__(self, send):
        self.bot = send

    def send_author(self):
        string='author.send'
        return string
    
    def send_channel(self):
        string='send'
        return string

def setup(bot):
    bot.add_cog(SendingMsg(bot))