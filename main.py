import discord
from discord.ext import commands
import specialist
from io import BytesIO

bot = commands.Bot(command_prefix="!")

# Setup listeners
@bot.listen()
async def on_ready():
    print("Bot is ready!")

@bot.listen()
async def on_message(message):
    print(f"<#{message.channel}> {message.author}: {message.content}") # Debugging
    await bot.process_commands(message) # Required or else it breaks with other commands

# Just a test command
@bot.command()
async def smd(ctx):
    await ctx.send(f"go fuck yourself {ctx.author}")

# FIXME: Need a way to write all this image data to a file AFTER it has been changed into raw bytes
#@bot.command()
#async def impact(ctx, topText, bottomText):
#    image = specialist.createTextOverlay(topText, bottomText, fontSize=25)
#    await ctx.send(file=discord.File(BytesIO(image), filename=f"le_epic_maymay_from_{ctx.author}.jpeg"))


bot.run("NzM3MTEzNDI4OTI5MjgyMTQ4.Xx4oYA.AtT25O2ApCku4KvVteU1k_9cg1o") # Start it UP
