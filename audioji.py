import os
import json
from time import ctime
import discord
from discord.ext import commands
import youtube_dl
import ffmpeg

# Initializes the audioji subfolder for a given server
def initSubfolder(guild: discord.Guild):
    print("[AUDIOJI] Beginning initialization...")
    if not os.path.exists("audioji"):
        print("[AUDIOJI] Folder doesn't exist! Making...")
        os.mkdir("audioji")
    try:
        print("[AUDIOJI] Creating guild folder and metadata...")
        os.mkdir(f"audioji/{guild.id}")
        with open(f"audioji/{guild.id}/meta.json", "w") as f: # Add a comment
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
    clipStart = float(clipStart)
    clipEnd = float(clipEnd)
    # Download the video
    print("[AUDIOJI] Downloading video...")
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
    print("[AUDIOJI] Extracting audio...")
    inputFile = ffmpeg.input("audio-tmp.mp4", ss=clipStart, to=clipEnd)
    output = ffmpeg.output(inputFile.audio, f"audioji/{ctx.guild.id}/{name}.mp3")
    ffmpeg.run(output)

    # Remove tempfile
    os.remove("audio-tmp.mp4")

    # Write metadata to folder
    print("[AUDIOJI] Writing metadata...")
    encoder = json.JSONEncoder(indent=4)
    # Not necessarily the most efficient way, as with long json files the operation time increases, but I don't think there's a better way other than with hashing
    data = ""
    with open(f"audioji/{ctx.guild.id}/meta.json", "r") as f: # why can't i open as read-write?
        data = json.load(f)
    with open(f"audioji/{ctx.guild.id}/meta.json", "w") as f:
        data["audiojis"][name] = {
            "author": ctx.author.name,
            "length": clipEnd-clipStart,
            "source": link,
            "creationDate": ctime()
        }
        f.write(encoder.encode(data))
    print(f"[AUDIOJI] Successfully created audioji '{name}' in file 'audioji/{ctx.guild.id}/{name}.mp3'.")

    await ctx.send(f"Successfully created audioji '{name}'!")
