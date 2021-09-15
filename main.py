import sys
import os
import re
import json

import discord
from discord.ext import commands
from discord.errors import LoginFailure
from discord_slash import SlashCommand
from PIL import Image
import youtube_dl

import rendering
import audioji
from details import details
import util

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)

# Setup listeners
@bot.listen()
async def on_ready():
    print("Bot is ready!")

# Realistically we only need this for logging/debugging
@bot.listen()
async def on_message(message):
    print(f"<#{message.channel}> {message.author}: {message.content}")

# TODO: Maybe we don't need this anymore? (Not going to clean this up)
#@bot.listen()
#async def on_command_error(ctx, error):
#    if type(error) == commands.errors.ExpectedClosingQuoteError:
#        await ctx.send(f"nice job with the quotation marks, {ctx.author.mention}")
#    elif type(error) == commands.errors.MissingRequiredArgument:
#        await ctx.send(f"You're missing some command arguments, {ctx.author.mention}.")
#    elif type(error) == commands.errors.CommandNotFound:
#        await ctx.send(f"The command you used doesn't exist! Check your spelling, {ctx.author.mention}.")
#    else:
#        await ctx.send(f"Error thrown! Tell the bot owner to check the logs.")
#        print(f"Error `{error}` of type `{type(error)}` pushed!")


# Just a test command
@slash.slash(
    name=details["smd"]["name"],
    description=details["smd"]["description"],
    options=details["smd"]["options"],
    guild_ids=guild_ids
)
async def smd(ctx, user="self"):
    if user == "self": # If the user inputs nothing
        user = ctx.author
    await ctx.send(f"go fuck yourself {user.mention}")

# Create impact font text on a blank background
@slash.slash(
    name=details["impact"]["name"],
    description=details["impact"]["description"],
    options=details["impact"]["options"],
    guild_ids=guild_ids
)
async def impact(ctx, top_text, bottom_text):
    # Make the image
    rawImage = rendering.createTextOverlay(top_text, bottom_text, fontSize=25)
    image = Image.frombytes("RGBA", rendering.SIZE, rawImage)
    tempFP = createTempFP(ctx, "png")

    # Save the image
    print("Saving image...")
    try:
        image.save(tempFP)
        print("Image saved correctly. Posting...")
        await ctx.send(file=discord.File(tempFP,
            filename=f"le_epic_maymay_from_{ctx.author}.jpeg"))
        os.remove(tempFP)
        print("Removed temporary file.")
    except OSError:
        print("Image failed to save, so not sent.")

# Creates the specialist meme and then sends it
@slash.slash(
    name=details["specialist"]["name"],
    description=details["specialist"]["description"],
    options=details["specialist"]["options"],
    guild_ids=guild_ids
)
async def specialist(ctx, top_text, bottom_text):
    await ctx.defer() # Working indicator

    tempFP = createTempFP(ctx, "mp4")

    # FIXME: Cleanup from last time using new temp system

    # Make sure it exists before screwing around
    if not os.path.exists("specialist.mp4"):
        print("Specialist not found! Make sure it's named "
            + "`specialist.mp4`.")
        return

    # Render it
    result = rendering.renderWithTextOverlay(
        "specialist.mp4",
        tempFP,
        rendering.createTextOverlay(top_text, bottom_text),
        14, 25
    )

    # Send it
    if result == 0:
        await ctx.send(
            file=discord.File(tempFP,
            filename=f"funny_specialist_meme_from_{ctx.author}.mp4")
        )
    else:
        print("Render failed, so not sending.")
        await ctx.send("Render failed. Please try again.")

    # Cleanup
    try:
        os.remove(tempFP)
    except OSError:
        print("Cleanup failed or temporary file did not exist in the "
            + "first place.")

# Adds impact font text to a Youtube video
@slash.slash(
    name=details["impact_video"]["name"],
    description=details["impact_video"]["description"],
    options=details["impact_video"]["options"],
    guild_ids=guild_ids
)
async def impact_video(ctx, link, top_text, bottom_text, start_time, end_time):
    await ctx.defer() # Working indicator
    
    ytTempFP = createTempFP(ctx, "impact-dl.mp4")
    overTempFP = createTempFP(ctx, "impact-over.mp4")


    # FIXME: Cleanup from last time using new temp system

    # Cleanup from before if cleanup failed last time
    #try:
    #    os.remove("ytdl-tmp.mp4")
    #    os.remove("overlain-tmp.mp4")
    #except: pass

    # All arguments come in as strings, so we'll need to change that
    start_time = float(start_time)
    end_time = float(end_time)

    # Limit length
    if end_time - start_time > 30:
        await ctx.send(f"{ctx.author.mention} Clip length is greater than "
            + "thirty seconds. Please make the clip shorter.")
    elif end_time - start_time <= 0:
        await ctx.send(f"{ctx.author.mention} Clip length is less than or "
            + "equal to 0 seconds. Please extend the clip.")

    # Download video
    ytdlOptions = {
        "format": "mp4",
        "outtmpl": ytTempFP # Set the name of the file
    }
    with youtube_dl.YoutubeDL(ytdlOptions) as ytdl:
        try: ytdl.download([link])
        except:
            await ctx.send(f"{ctx.author.mention} Link is incorrect. "
                + "Please try another link.")
            return 1

    # Render
    result = rendering.renderWithTextOverlay(
        ytTempFP,
        overTempFP,
        rendering.createTextOverlay(top_text, bottom_text),
        start_time, end_time
    )

    # Send it
    if result == 0:
        await ctx.send(
            file=discord.File(overTempFP,
            filename=f"funny_clip_meme_from_{ctx.author}.mp4")
        )
    elif result == 1:
        await ctx.send(f"{ctx.author.mention} Clip length exceeds length "
            + "of the video. Please adjust clip restraints.")
    else:
        await ctx.send(f"{ctx.author.mention} Clip failed to render. "
            + "Please try again.")

    # Cleanup
    try:
        os.remove(ytTempFP)
        os.remove(overTempFP)
    except OSError:
        print("Cleanup failed or temporary file did not exist in the "
            + "first place.")

@slash.slash(
    name=details["word_occurrences"]["name"],
    description=details["word_occurrences"]["description"],
    options=details["word_occurrences"]["options"],
    guild_ids=guild_ids
)
async def word_occurrences(ctx, user, word, channel=None, limit=1000):
    await ctx.defer()

    limit = int(limit)

    # If a channel is not specified, use the current context
    if not channel:
        channel = ctx.channel
    elif channel == "all": # Use for later, make sure we don't catch it now
        pass
    elif not type(channel) is discord.TextChannel: # If the wrong channel type was passed
        print(f"[ERROR] Non-text channel {channel.name} passed!")
        await ctx.send("Non-text channel passed! Make sure to "
            + "choose a text channel.")
        return 1

    # Main func
    async def _countMessages(channel):
        print(f"Getting the past {limit} messages from {channel.name}...")
        # Get all messages, extract message content, and only use ones
        # created by a certain user
        messages = []
        try:
            messages = await channel.history(limit=limit).flatten()
            messages = [message.content for message in messages
                if user == message.author]
        except discord.Forbidden:
            print("[ERROR] Bot doesn't have the correct permissions "
                + f"to access channel {channel.name}!")
            raise Exception() # lol idk how to use discord.Forbidden
            return 0

        print(f"Counting {len(messages)} messages...")
        # Count messages
        count = 0
        for message in messages:
            # Add all occurrances of the word in the message to the count
            # (case insensitive)
            print(f"Message: {message}")
            count += len(re.findall(word, message, flags=re.I))
        print(count)
        return count


    if channel == "all":
        await ctx.send(f"Checking the past {limit} messages from ALL "
            + "channels! This may take some time, so take a seat and "
            + "relax!")
        channels = [x for x in ctx.guild.channels
            if type(x) == discord.TextChannel]
        print(f"Getting the past {limit} messages from ALL "
            + f"{len(ctx.guild.channels)} channels."
            + "\nWARNING: This may take a long time!")
        count = 0
        forbiddenChannels = []
        for channel in channels:
            try:
                count += await _countMessages(channel)
            except Exception:
                forbiddenChannels.append(channel)
        await ctx.send(f"{user.mention} has used the word `{word}` "
            + f"***{count} times*** within the past {limit} "
            + "messages within all channels.")
        if len(forbiddenChannels):
            errorMessage = "The bot could not access the following " \
            + "channels, so the channels were not counted: \n```"
            for forbiddenChannel in forbiddenChannels:
                errorMessage += f"\n{forbiddenChannel.name}"
            errorMessage += "\n```"
            await ctx.send(errorMessage)
    else:
        try:
            count = await _countMessages(channel)
            await ctx.send(f"{user.mention} has used the word `{word}` "
                + f"***{count} times*** within the past {limit} messages "
                + f"in the channel {channel.mention}.")
        except Exception:
            await ctx.send("The bot doesn't have permissions to post "
                + "to this channel! Make sure it has the \"Read Message "
                + "History\" permissions before trying to connect to this "
                + "channel again.")


# Audioji group
#@bot.group(name="audioji")
#async def _audioji(ctx):
#    pass

# Make sure the subfolder is init'd before starting
async def _audiojiPreinvoke(ctx):
    if not os.path.exists(f"audioji/{ctx.guild.id}"):
        audioji.initSubfolder(ctx.guild)

# TODO: Doesn't disconnect, but doesn't push error?
async def _audiojiPostinvoke(ctx): # Get out of voice chat if in it
    try: await ctx.voice_client.disconnect()
    except AttributeError: pass
    except: print("[ERROR] Other audioji postivnoke error!")

# this is really stupid and should affect the coruotine;
# kinda ruins the point of a decorator
#@_audioji.before_invoke(_audiojiPreinvoke)
#@_audioji.after_invoke(_audiojiPostinvoke)

@slash.subcommand(
    base="audioji",
    base_desc="Plays audio clips in your voice chat.",
    name=details["audioji_add"]["name"],
    description=details["audioji_add"]["description"],
    options=details["audioji_add"]["options"],
    guild_ids=guild_ids
)
async def _add(ctx, name, link, clipStart, clipEnd):
    await ctx.defer()
    # ehhh could be better
    await audioji.addNewAudioji(ctx, name, link, clipStart, clipEnd)

    # Update audioji commands
    print("Forcing update of audioji commands!")
    for id in guild_ids:
        print(f"Updating audioji commands for guild {id}...")
        audioji.updateAudiojiSlashCommand(_play, "play", slash, id)
        audioji.updateAudiojiSlashCommand(_info, "play", slash, id)

@slash.subcommand(
    base="audioji",
    base_desc="Plays audio clips in your voice chat.",
    name=details["audioji_play"]["name"],
    description=details["audioji_play"]["description"],
    options=details["audioji_play"]["options"],
    guild_ids=guild_ids
)
async def _play(ctx, name):
    await audioji.playAudioji(ctx, name)

@slash.subcommand(
    base="audioji",
    base_desc="Plays audio clips in your voice chat.",
    name=details["audioji_list"]["name"],
    description=details["audioji_list"]["description"],
    options=details["audioji_list"]["options"],
    guild_ids=guild_ids
)
async def _list(ctx):
    list = ""
    audiojis = []
    with open(f"audioji/{ctx.guild.id}/meta.json", "r") as f:
        audiojis = json.load(f)
    audiojis = audiojis["audiojis"] # Get the actual list

    if len(audiojis) == 0: # If you ain't got none
        await ctx.send("There are no audiojis! Get to making with "
            + "`!audioji add`!")
        return 1

    # Make the list
    # No I'm not going to add an edgecase for one audioji (or maybe I will)
    list += f"There are {len(audiojis)} Audiojis: \n```\n"
    for name, data in audiojis.items():
        list += f"\n'{name}', by {data['author']}"
    list += "\n```"

    await ctx.send(list)

@slash.subcommand(
    base="audioji",
    base_desc="Plays audio clips in your voice chat.",
    name=details["audioji_info"]["name"],
    description=details["audioji_info"]["description"],
    options=details["audioji_info"]["options"],
    guild_ids=guild_ids
)
async def _info(ctx, name):
    await ctx.send(embed=audioji.formatAudiojiEmbed(ctx.guild, name))


try: bot.run(sys.argv[1]) # Start it UP
except LoginFailure:
    print("Invalid bot token!\n"
        + "Please make sure you're using the correct token,"
        + "and use quotes if you have to.")
except IndexError:
    print("Empty bot token!\nPlease make sure to enter in your bot token.")
