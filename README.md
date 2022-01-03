# Discord Specialist Bot

*A multifunctional media bot*

---

## What is this?
`discord-specialist-bot` is a bot for Discord. It was originally meant to apply impact font text to the [Persona 4 Specialist meme](https://www.youtube.com/watch?v=fTczCpIaLAU), but spiralled into a multifunctional bot for my own personal use. Now, it has come out of private to be a public repository to show my Python knowledge and a bot access token from when I first started this (yes, it is there; no, it is not active).

## What can it do?
- Act as a community-curated soundboard
- Rudimentally play audio from a certain website
- Perform parry mechanics
- Clip and add impact font text to videos from the internet

## What do I need?
- Python 3.8 (at least)
- `youtube-dl`
- `Pillow`
- `discord.py`
- `discord-py-slash-command`
- `ffmpeg-python`
- `opencv-python-headless` or `opencv-python` (which is superfluous and whose inclusion may be deprecated when I get to working onit)
- A Discord bot (which I will not detail how to do)
- The Impact font `.ttf` file, named `impact.ttf` in the root folder of this repository
- An `.mp4` file of Specialist from Persona 4, named `specialist.mp4` in the root folder of this repository

## Usage
Just use

```
python main.py [YOUR_BOT_TOKEN_HERE]
```

and it will start itself. Remember to have `impact.ttf` and `specialist.mp4` in the root of this directory, or things will not work correctly.

## FAQs
### Will this ever be on [insert popular bot site here]?
No. I don't think I'll ever host it on any bot site, and this script is meant for more niche, personal use. If this is on a bot hosting site, you'll know it wasn't me.

### Will you add *X* feature?
No. Do it yourself :)

### Will you fix *Y* bug?
More likely. Put in an issue request with the logs produced by the script and means of reproducing the error, and then I'll get to it eventually (probably).

## Licensing
`discord-specialist-bot` is licensed under the MIT license, which can be found in `LICENSE`.

