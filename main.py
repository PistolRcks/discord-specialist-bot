import sys
import os
import re
import json
import discord
from discord.ext import commands
from discord.errors import LoginFailure
from PIL import Image
import youtube_dl
import rendering
import audioji
import helptext

bot = commands.Bot(command_prefix="!")

# Setup listeners
@bot.listen()
async def on_ready():
    print("Bot is ready!")

@bot.listen()
async def on_message(message):
    print(f"<#{message.channel}> {message.author}: {message.content}") # Debugging

@bot.listen()
async def on_command_error(ctx, error):
    if type(error) == commands.errors.ExpectedClosingQuoteError:
        await ctx.send(f"nice job with the quotation marks, {ctx.author.mention}")
    elif type(error) == commands.errors.MissingRequiredArgument:
        await ctx.send(f"You're missing some command arguments, {ctx.author.mention}.")
    elif type(error) == commands.errors.CommandNotFound:
        await ctx.send(f"The command you used doesn't exist! Check your spelling, {ctx.author.mention}.")
    else:
        await ctx.send(f"Error thrown! Tell the bot owner to check the logs.")
        print(f"Error `{error}` of type `{type(error)}` pushed!")


# Just a test command
@bot.command(description=helptext.help["smd"]["desc"], usage=helptext.formatUsage("smd"), help=helptext.formatHelptext("smd"), brief=helptext.help["smd"]["desc"])
async def smd(ctx, user="self"):
    if user == "self": # If the user inputs nothing
        user = ctx.author.mention
    elif not re.match(r"<@", user): # If the user is not directly mentioned (with an @)
        try:
            user = [member.mention for member in ctx.guild.members \
                if member.name == re.sub(r"(?=#).+$", "", user) \
                and member.discriminator == re.sub(r"^.+(?<=#)", "", user)][0]
        except:
            ctx.send("Could not find user! Try again.")
            return 1
    await ctx.send(f"go fuck yourself {user}")

# Create impact font text on a blank background
@bot.command(description=helptext.help["impact"]["desc"], usage=helptext.formatUsage("impact"), help=helptext.formatHelptext("impact"), brief=helptext.help["impact"]["desc"])
async def impact(ctx, topText, bottomText):
    async with ctx.typing(): # Working indicator
        # Make the image
        rawImage = rendering.createTextOverlay(topText, bottomText, fontSize=25)
        image = Image.frombytes("RGBA", rendering.SIZE, rawImage)

        # Save the image
        print("Saving image...")
        try:
            image.save("img-tmp.png")
            print("Image saved correctly. Posting...")
            await ctx.send(file=discord.File("img-tmp.png", filename=f"le_epic_maymay_from_{ctx.author}.jpeg"))
            os.remove("img-tmp.png")
            print("Removed temporary file.")
        except OSError:
            print("Image failed to save, so not sent.")

# Creates the specialist meme and then sends it
@bot.command(description=helptext.help["specialist"]["desc"], usage=helptext.formatUsage("specialist"), help=helptext.formatHelptext("specialist"), brief=helptext.help["specialist"]["desc"])
async def specialist(ctx, topText, bottomText):
    async with ctx.typing(): # Working indicator
        # Make sure it exists before screwing around
        if not os.path.exists("specialist.mp4"):
            print("Specialist not found! Make sure it's named `specialist.mp4`.")
            pass
        # Cleanup if command failed last time
        try: os.remove("specialist-tmp.mp4")
        except: pass

        # Render it
        result = rendering.renderWithTextOverlay("specialist.mp4", "specialist-tmp.mp4", \
            rendering.createTextOverlay(topText, bottomText), \
            14, 25)

        # Send it
        if result == 0:
            await ctx.send(file=discord.File("specialist-tmp.mp4", filename=f"funny_specialist_meme_from_{ctx.author}.mp4"))
        else:
            print("Render failed, so not sending.")
            await ctx.send("Render failed. Please try again.")

        # Cleanup
        try: os.remove("specialist-tmp.mp4")
        except OSError: print("Cleanup failed or temporary file did not exist in the first place.")

# Adds impact font text to a Youtube video
@bot.command(description=helptext.help["impact_video"]["desc"], usage=helptext.formatUsage("impact_video"), help=helptext.formatHelptext("impact_video"), brief=helptext.help["impact_video"]["desc"])
async def impact_video(ctx, link, topText, bottomText, startTime, endTime):
    async with ctx.typing(): # Working indicator

        # Cleanup from before if cleanup failed last time
        try:
            os.remove("ytdl-tmp.mp4")
            os.remove("overlain-tmp.mp4")
        except: pass

        # All arguments come in as strings, so we'll need to change that
        startTime = float(startTime)
        endTime = float(endTime)

        # Limit length
        if endTime - startTime > 30:
            await ctx.send(f"{ctx.author.mention} Clip length is greater than thirty seconds. Please make the clip shorter.")
        elif endTime - startTime <= 0:
            await ctx.send(f"{ctx.author.mention} Clip length is less than or equal to 0 seconds. Please extend the clip.")

        # Download video
        ytdlOptions = {
            "format": "mp4",
            "outtmpl": "ytdl-tmp.mp4" # Set the name of the file
        }
        with youtube_dl.YoutubeDL(ytdlOptions) as ytdl:
            try: ytdl.download([link])
            except:
                await ctx.send(f"{ctx.author.mention} Link is incorrect. Please try another link.")
                return 1

        # Render
        result = rendering.renderWithTextOverlay("ytdl-tmp.mp4", "overlain-tmp.mp4", \
            rendering.createTextOverlay(topText, bottomText), \
            startTime, endTime)

        # Send it
        if result == 0:
            await ctx.send(file=discord.File("overlain-tmp.mp4", filename=f"funny_clip_meme_from_{ctx.author}.mp4"))
        elif result == 1:
            await ctx.send(f"{ctx.author.mention} Clip length exceeds length of video. Please adjust clip restraints.")
        else:
            await ctx.send(f"{ctx.author.mention} Clip failed to render. Please try again.")

        # Cleanup
        try:
            os.remove("ytdl-tmp.mp4")
            os.remove("overlain-tmp.mp4")
        except OSError: print("Cleanup failed or temporary file did not exist in the first place.")

# Audioji group
@bot.group(name="audioji")
async def _audioji(ctx):
    pass

async def _audiojiPreinvoke(ctx): # Make sure the subfolder is init'd before starting
    if not os.path.exists(f"audioji/{ctx.guild.id}"):
        audioji.initSubfolder(ctx.guild)

@_audioji.before_invoke(_audiojiPreinvoke) # this is really stupid and should affect the coruotine; kinda ruins the point of a decorator

@_audioji.command(name="add", description=helptext.help["audioji_add"]["desc"], usage=helptext.formatUsage("audioji_add"), help=helptext.formatHelptext("audioji_add"), brief=helptext.help["audioji_add"]["desc"])
async def _add(ctx, name, link, clipStart, clipEnd):
    async with ctx.typing():
        await audioji.addNewAudioji(ctx, name, link, clipStart, clipEnd) # ehhh could be better

@_audioji.command(name="play", description=helptext.help["audioji_play"]["desc"], usage=helptext.formatUsage("audioji_play"), help=helptext.formatHelptext("audioji_play"), brief=helptext.help["audioji_play"]["desc"])
async def _play(ctx, target):
    async with ctx.typing():
        await audioji.playAudioji(ctx, target)

@_audioji.command(name="list", description=helptext.help["audioji_list"]["desc"], usage="", help="", brief=helptext.help["audioji_list"]["desc"])
async def _list(ctx):
    list = ""
    audiojis = []
    with open(f"audioji/{ctx.guild.id}/meta.json", "r") as f:
        audiojis = json.load(f)
    audiojis = audiojis["audiojis"] # Get the actual list

    if len(audiojis) == 0: # If you ain't got none
        await ctx.send("There are no audiojis! Get to making with `!audioji add`!")
        return 1

    # Make the list
    list += f"There are {len(audiojis)} Audiojis: \n```\n" # No I'm not going to add an edgecase for one audioji (or maybe I will)
    for name, details in audiojis.items():
        list += f"\n'{name}', by {details['author']}"
    list += f"\n```"

    await ctx.send(list)

# Shows audioji metadata
@_audioji.command(name="info", description=helptext.help["audioji_info"]["desc"], usage=helptext.formatUsage("audioji_info"), help=helptext.formatHelptext("audioji_info"), brief=helptext.help["audioji_info"]["desc"])
async def _info(ctx, target):
    await ctx.send(embed=audioji.formatAudiojiEmbed(ctx.guild, target))


try: bot.run(sys.argv[1]) # Start it UP
except LoginFailure: print("Invalid bot token!\nPlease make sure you're using the correct token, and use quotes if you have to.")
except IndexError: print("Empty bot token!\nPlease make sure to enter in your bot token.")
