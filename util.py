from asyncio import TimeoutError
import traceback
from time import time

import discord

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

    return f"tmp/{ctx.command[:4]}-{ctx.guild.id}-{str(time())[-8:]}.tmp.{ext}"

# Attempts to connect to a voice channel. Returns an int return code or the Client.
async def connectToVoice(ctx):    
    # Try to get the channel the evoker is in
    channel = ""
    try:
        channel = ctx.author.voice.channel # Invoked voice channel
    except AttributeError: # If not connected
        await ctx.send("You are not in a voice channel! "
            + f"{ctx.author.mention}, please join a voice channel before "
            + "executing the command.")


    # Attempt to connect
    client = ""
    try:
        client = await channel.connect()
    except TimeoutError:
        print("[ERROR] Timed out while trying to connect to voice"
            + f"channel {channel.name}.")
        await ctx.send("Timed out while trying to connect!")
        return 2
    except discord.ClientException:
        if not channel == ctx.guild.voice_client.channel: # Invoked voice channel vs
                                                    # actual voice channel
            await ctx.guild.voice_client.move_to(channel)
            client = ctx.guild.voice_client
        else: # i.e. the currently connected channel is the invoked channel
            client = ctx.guild.voice_client
    except RuntimeError as e: # Whenever a dependency is not installed
        print("PyNaCl or some other dependency is probably not "
            + "installed.\nStack Trace:")
        traceback.print_tb(e.__traceback__)
        await ctx.send("Sorry, we couldn't connect right now."
            + "Your bot owner needs to update the dependencies for this bot!")
        return 3
    except Exception as e: # Fallthrough
        aprint("[ERROR] Fatally failed to connect to voice channel "
            + f"{channel.name}.\nStack Trace:")
        traceback.print_tb(e.__traceback__)
        await ctx.send("Exceptionally failed to connect to a voice channel!")
        return 4

    return client

