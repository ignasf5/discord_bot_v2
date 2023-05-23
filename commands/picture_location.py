import os
from discord.ext import commands

PICTURES = os.environ['PICTURES_PATH']

class picture(commands.Cog):
    def __init__(self, picture_name):
        self.client = picture_name

    def get_picture(self, picture_name):
        picture_path = os.path.join(PICTURES, picture_name)
        if os.path.isfile(picture_path):
            return picture_path
        else:
            return None
        
class picture_with_path(commands.Cog):
    def __init__(self, picture_name):
        self.client = picture_name

    def get_picture_path(self, picture_name, folder=None):
        if folder:
            picture_path = os.path.join(PICTURES, folder, picture_name)
        else:
            picture_path = os.path.join(PICTURES, picture_name)
        if os.path.isfile(picture_path):
            return picture_path
        else:
            return None

def setup(client):
    client.add_cog(picture(client))
    client.add_cog(picture_with_path(client))