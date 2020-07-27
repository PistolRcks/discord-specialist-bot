import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="!")

# Setup listeners
@bot.listen()
async def on_ready():
    print("Bot is ready!")

@bot.listen()
async def on_message(message):
    print(f"<#{message.channel}> {message.author}: {message.content}") # Debugging
    await bot.process_commands(message) # Required or else it breaks with other commands

@bot.command()
async def smd(ctx):
    await ctx.send(f"go fuck yourself {ctx.author}")

bot.run("NzM3MTEzNDI4OTI5MjgyMTQ4.Xx4oYA.AtT25O2ApCku4KvVteU1k_9cg1o") # Start it UP
