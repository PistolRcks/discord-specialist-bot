# Discord bot audioji (audio soundclips) module
import os
import json
from time import ctime

import discord
import discord_slash
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType as OptionType
import youtube_dl
import ffmpeg

from details import details
import util

# Adding a wrapper to print to prepend, makes things look nicer
def aprint(str):
    print(f"[AUDIOJI] {str}")

# Initializes the audioji subfolder for a given server
def initSubfolder(guild: discord.Guild):
    aprint("Beginning initialization...")
    if not os.path.exists("audioji"):
        aprint("Folder doesn't exist! Making...")
        os.mkdir("audioji")
    try:
        aprint("Creating guild folder and metadata...")
        os.mkdir(f"audioji/{guild.id}")
        with open(f"audioji/{guild.id}/meta.json", "w") as f: # Add a comment
            encoder = json.JSONEncoder(indent=4)
            f.write(encoder.encode({
                "_guildInfo" : "Metadata for audiojis for the Discord "
                    + f"server {guild.name} (ID: {guild.id})",
                "audiojis" : {}
            }))
    except IOError:
        aprint("[ERROR] Folder already exists! Stopping...")
    except OSError:
        aprint("[ERROR] File/folder creation error! Make sure the folder "
            + "the bot is in has read/write permissions.")

async def addNewAudioji(ctx, name, link, clipStart, clipEnd):
    """ Adds a new audioji from a YouTube video, renders it to mp3, and writes
        metadata.

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
    tempFP = util.createTempFP(ctx, ".mp4")

    aprint("Downloading video...")
    ytdlOptions = {
        "format": "mp4",
        "outtmpl": tempFP # Set the name of the file
    }
    with youtube_dl.YoutubeDL(ytdlOptions) as ytdl:
        try: ytdl.download([link])
        except:
            aprint("Incorrect link or youtube-dl out of date.")
            await ctx.send(f"{ctx.author.mention} Link is incorrect. Please try another link.")
            return 1

    # Extract the audio (as .mp3) and render to correct folder
    aprint("Extracting audio...")
    inputFile = ffmpeg.input(tempFP, ss=clipStart, to=clipEnd)
    output = ffmpeg.output(inputFile.audio, f"audioji/{ctx.guild.id}"
        + f"/{name}.mp3")
    output = ffmpeg.overwrite_output(output) # Overwrite for better
                                             # audioji editing
    ffmpeg.run(output)

    # Remove tempfile
    os.remove(tempFP)

    # Write metadata to folder
    aprint("Writing metadata...")
    encoder = json.JSONEncoder(indent=4)
    # Not necessarily the most efficient way, as with long json files the
    # operation time increases, but I don't think there's a better way other
    # than with hashing
    data = ""
    # why can't i open as read-write?
    with open(f"audioji/{ctx.guild.id}/meta.json", "r") as f:
        data = json.load(f)
    with open(f"audioji/{ctx.guild.id}/meta.json", "w") as f:
        data["audiojis"][name] = {
            "author": ctx.author.name,
            "length": clipEnd-clipStart,
            "source": link,
            "creationDate": ctime()
        }
        f.write(encoder.encode(data))
    aprint(f"Successfully created audioji '{name}' in file 'audioji" +
        f"/{ctx.guild.id}/{name}.mp3'.")

    await ctx.send(f"Successfully created audioji '{name}'!")
    return 0

# Plays an audioji
async def playAudioji(ctx, target):
    # Check and see if there actually is an audioji of that name
    if not os.path.isfile(f"audioji/{ctx.guild.id}/{target}.mp3"):
        aprint(f"[ERROR] Audioji \"{target}.mp3\" for the guild "
            + f"\"{ctx.guild.id}\" doesn't exist.")
        await ctx.send("The audioji that you requested doesn't exist!\n"
            + "Find another audioji using `!audioji list` or make a new one "
            + "using `!audioji add`!")
        return 1

    # Connect to voice
    client = await util.connectToVoice(ctx)
    assert(client is not int) # Make sure we didn't pull an error

    audio = discord.FFmpegPCMAudio(f"audioji/{ctx.guild.id}/{target}.mp3")
    try:
        await ctx.send(f"Successfully played audioji `{target}`.", hidden=True)
        client.play(audio)
    except discord.ClientException: # If there is already something playing, parry it
        client.stop()
        await ctx.send("Parried!")
        client.play(audio)
    return 0

# Makes an embed to show a target audioji's metadata
def formatAudiojiEmbed(guild, target):
    # Open up the metadata file
    data = ""
    with open(f"audioji/{guild.id}/meta.json") as f:
        data = json.load(f)
    audioji = data["audiojis"][target]

    # Generate the embed
    embed = discord.Embed(
        title=target,
        type="rich",
        description="This is the information for this audioji.",
        color=discord.Colour.blurple()
    )

    # Add the fields to the embed
    (
        embed.add_field(name="Author", value=audioji["author"])
        .add_field(name="Clip Length", value=f"{audioji['length']} sec")
        .add_field(name="Source", value=audioji["source"])
        .add_field(name="Creation Date", value=audioji["creationDate"])
    )

    return embed
