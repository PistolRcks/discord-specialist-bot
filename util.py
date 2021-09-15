import discord
from time import time

def createTempFP(ctx, ext):
    """ Generate a string to use as a temporary filename (and filepath)
        Parameters:
            ctx (discord.ext.commands.Context): The context in which the command 
                which requires a temporary file is performed.
            ext (str): The name of the file extension being used.
        Returns:
            A string which represents a filepath from the root directory of the bot
            into the temporary folder `tmp`.
    """
    
    """ Append the following (separated some times by dashes):
        - "tmp/"
        - The originating command (truncated to 4 characters, from the beginning)
        - The id of the guild (server)
        - The current epoch (truncated to 8 digits, from the end)
        - ".tmp."
        - The file extension
    """

    return f"tmp/{ctx.command.name[:4]}-{ctx.guild.id}-{str(time())[-8:]}.tmp.{ext}"
