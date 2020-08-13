import os
import json
import discord
from discord.ext import commands
import youtube_dl
import ffmpeg

# Initializes the audioji subfolder for a given server
def initSubfolder(guild: discord.Guild):
    if not os.exists("audioji"):
        os.mkdir("audioji")
    try:
        os.mkdir(f"audioji/{guild.id}")
        with f as os.open("audioji/{guild.id}/meta.json", "rw"): # Add a comment
            encoder = json.JSONEncoder(indent=4)
            f.write(encoder.encode({"_guildInfo" : f"Metadata for audiojis for the Discord server {guild.name} (ID: {guild.id})", "audiojis" : {}})
    except os.FileExistsError:
        print("[ERROR] Folder already exists! Stopping...)
        pass
    except OSError:
        print("[ERROR] File/folder creation error! Make sure the folder the bot is in has read/write permissions.")
        pass

def addNew(name, ytLink, clipStart, clipEnd):
    pass #TODO
    
