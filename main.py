import sys
import os
from io import BytesIO
import discord
from discord.ext import commands
from discord.errors import LoginFailure
from PIL import Image
import specialist

bot = commands.Bot(command_prefix="!")

# Setup listeners
@bot.listen()
async def on_ready():
    print("Bot is ready!")

@bot.listen()
async def on_message(message):
    print(f"<#{message.channel}> {message.author}: {message.content}") # Debugging

# Just a test command
@bot.command()
async def smd(ctx):
    await ctx.send(f"go fuck yourself {ctx.author}")

# Create impact font text on a blank background
@bot.command()
async def impact(ctx, topText, bottomText):
	# Make the image
	rawImage = specialist.createTextOverlay(topText, bottomText, fontSize=25)
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


try: bot.run(sys.argv[1]) # Start it UP
except LoginFailure: print("Invalid bot token!\nPlease make sure you're using the correct token, and use quotes if you have to.")
except IndexError: print("Empty bot token!\nPlease make sure to enter in your bot token.")
