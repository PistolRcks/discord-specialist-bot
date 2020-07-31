import sys
import os
from io import BytesIO
import discord
from discord.ext import commands
from discord.errors import LoginFailure
from PIL import Image
import rendering

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
        await ctx.send(f"you're missing some command arguments, {ctx.author.mention}")
    else:
        print(f"Error `{error}` of type `{type(error)}` pushed!")


# Just a test command
@bot.command()
async def smd(ctx):
    await ctx.send(f"go fuck yourself {ctx.author.mention}")

# Create impact font text on a blank background
@bot.command()
async def impact(ctx, topText, bottomText):
	# Make the image
	rawImage = rendering.createTextOverlay(topText, bottomText, fontSize=25)
	image = Image.frombytes("RGBA", specialist.SIZE, rawImage)

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
@bot.command()
async def specialist(ctx, topText, bottomText):
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


try: bot.run(sys.argv[1]) # Start it UP
except LoginFailure: print("Invalid bot token!\nPlease make sure you're using the correct token, and use quotes if you have to.")
except IndexError: print("Empty bot token!\nPlease make sure to enter in your bot token.")
