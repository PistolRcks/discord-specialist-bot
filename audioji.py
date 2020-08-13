import os
import json
from time import ctime
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
        with open(f"audioji/{guild.id}/meta.json", "rw") as f: # Add a comment
            encoder = json.JSONEncoder(indent=4)
            f.write(encoder.encode({
                "_guildInfo" : f"Metadata for audiojis for the Discord server {guild.name} (ID: {guild.id})",
                "audiojis" : {}
            }))
    except IOError:
        print("[ERROR] Folder already exists! Stopping...")
    except OSError:
        print("[ERROR] File/folder creation error! Make sure the folder the bot is in has read/write permissions.")

async def addNew(ctx, name, link, clipStart, clipEnd):
    # Download the video
    ytdlOptions = {
        "format": "mp4",
        "outtmpl": "audio-tmp.mp4" # Set the name of the file
    }
    with youtube_dl.YoutubeDL(ytdlOptions) as ytdl:
        try: ytdl.download([link])
        except:
            print("[ERROR] Incorrect link or youtube-dl out of date.")
            await ctx.send(f"{ctx.author.mention} Link is incorrect. Please try another link.")
            return 1

    # Extract the audio (as .mp3) and render to correct folder
    inputFile = ffmpeg.input("audio-tmp.mp4", ss=clipStart, to=clipEnd)
    output = ffmpeg.output(inputFile.audio, f"audioji/{ctx.guild.id}/{name}.mp3")
    ffmpeg.run(output)

    # Remove tempfile
    os.remove("audio-tmp.mp4")

    # Write metadata to folder
    encoder = json.JSONEncoder(indent=4)
    # Not necessarily the most efficient way, as with long json files the operation time increases, but I don't think there's a better way other than with hashing
    with open(f"audioji/{ctx.guild.id}/meta.json", "rw") as f:
        data = json.load(f)
        data["audiojis"][name] = {
            "author": ctx.author,
            "length": clipEnd-clipStart,
            "source": link,
            "creationDate": ctime()
        }
        f.write(encoder.encode(data))
