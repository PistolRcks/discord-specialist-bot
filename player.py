# Module for playing and queuing YouTube videos
# Directly stolen from https://stackoverflow.com/questions/60745020/is-there-a-way-to-directly-stream-audio-from-a-youtube-video-using-youtube-dl-or

# TODO: Queuing
# TODO: Playback commands
# TODO: Playlists
# TODO: Playing audioji over music?

import discord
import youtube_dl

import util

async def playVideo(ctx, link):
    """ Plays a YouTube video.
        Parameters:
            ctx (discord.ext.commands.Context): The context in which the command was invoked.
            link (str): The link to the YouTube video to play.
    """
    
    # Get the direct download link
    directLink = ""
    info = []
    with youtube_dl.YoutubeDL() as ydl:
        try: info = ydl.extract_info(link, download = False)
        except:
            print("Incorrect link or youtube-dl out of date.")
            await ctx.send(f"{ctx.author.mention} Link is incorrect. Please try another link.", hidden=True)
            return 1

        # Only play the best one which actually has audio
        formats = [f for f in info["formats"] if f["acodec"] != "none"] 
        directLink = info["formats"][-1]["url"]

    print(directLink)

    # Connect to voice
    client = await util.connectToVoice(ctx)
    assert(client is not int) # Make sure we didn't pull an error

    # TODO: Perhaps this could be in `util.py` as well...
    audio = discord.FFmpegPCMAudio(directLink)
    await ctx.send(f"Playing Youtube video `{info['title']}`", hidden=True)
    client.play(audio)
    return 0



