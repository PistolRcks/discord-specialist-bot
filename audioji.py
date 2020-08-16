# Discord bot audioji (audio soundclips) module
import os
import json
from time import ctime
from asyncio import TimeoutError
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

async def addNewAudioji(ctx, name, link, clipStart, clipEnd):
    """ Adds a new audioji from a YouTube video, renders it to mp3, and writes metadata.

    Parameters:
        ctx (discord.Context): The context in which the command was invoked.
        name (str): The name which to name the audioji.
        link (str): The link with which to create the audio for the audioji.
        clipStart (float): Indicates the beginning of the clip.
        clipEnd (float): Indicates the end of the clip.

    Returns:
        An integer error code.
        0 is OK.
        1 is a youtube-dl failure.
    """
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
    output = ffmpeg.overwrite_output(output) # Overwrite for better audioji editing
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
    return 0

# Plays an audioji
async def playAudioji(ctx, target):
    channel = ""
    try:
        channel = ctx.author.voice.channel # Invoked voice channel
    except AttributeError: # If not connected
        await ctx.send(f"You are not in a voice channel! {ctx.author.mention}, please join a voice channel before executing the command.")

    client = ""
    try:
        client = await channel.connect()
    except TimeoutError:
        print("f[ERROR] Timed out while trying to connect to voice channel {channel.name}.")
        await ctx.send("Timed out while trying to connect!")
        return 1
    except discord.ClientException:
        if not channel == ctx.voice_client.channel: # Invoked voice channel vs actual voice channel
            await ctx.voice_client.move_to(channel)
            client = ctx.voice_client
        else: # i.e. the currently connected channel is the invoked channel
            client = ctx.voice_client
    except:
        print(f"[ERROR] Fatally failed to connect to voice channel {channel.name}.")
        await ctx.send("Exceptionally failed to connect to a voice channel!")
        return 2

    audio = discord.FFmpegPCMAudio(f"audioji/{ctx.guild.id}/{target}.mp3")
    client.play(audio)
    # Client will disconnect after code execution. Don't worry.

# Makes an embed to show a target audioji's metadata
def formatAudiojiEmbed(guild, target):
    data = ""
    with open(f"audioji/{guild.id}/meta.json") as f:
        data = json.load(f)
    audioji = data["audiojis"][target]
    embed = discord.Embed(title=target, type="rich", description="This is the information for this audioji.", color=discord.Colour.blurple())
    (
        embed.add_field(name="Author", value=audioji["author"])
        .add_field(name="Clip Length", value=f"{audioji['length']} sec")
        .add_field(name="Source", value=audioji["source"])
        .add_field(name="Creation Date", value=audioji["creationDate"])
    )
    return embed
