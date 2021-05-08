# Provides the details for slash commands for the bot
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType as OptionType

# Holds the details (name, description, arguments) for all the slash commands
details = {
    "smd" : {
        # Name of the command
        # NB: This CANNOT contain capital letters.
        "name" : "smd",

        # Short description of the command's behavior
        "description" : "Tells the user to fuck off "
            + "(or, if a user is not supplied, tells you to fuck off).",

        # Positional arguments (in order of position) in a list (previously "args")
        # NB: These are passed as kwargs to their underlying functions, so they should
        # be the same name as the parameters for those functions.
        "options" : [
            create_option(
                name="user", # Name of the argument
                description="User to tell to fuck off.", # Description of the argument's use
                option_type=OptionType.USER,    # Type of the argument
                required=False   # Whether or not the argument is required
            )
        ]
    },
    "impact" : {
        "name" : "impact",
        "description" : "Creates impact font text on a blank background.",
        "options" : [
            create_option(
                name="top_text",
                description="Text to put on the top. (Automatically capitalized.)",
                option_type=OptionType.STRING,
                required=True
            ),
            create_option(
                name="bottom_text",
                description="Text to put on the bottom. (Automatically capitalized.)",
                option_type=OptionType.STRING,
                required=True
            )
        ]
    },
    "specialist" : {
        "name" : "specialist",
        "description" : "Creates a video of the song 'specialist' with Impact font text overlain.",
        "options" : [
            create_option(
                name="top_text",
                description="Text to put on the top. (Automatically capitalized.)",
                option_type=OptionType.STRING,
                required=True
            ),
            create_option(
                name="bottom_text",
                description="Text to put on the bottom. (Automatically capitalized.)",
                option_type=OptionType.STRING,
                required=True
            )
        ]
    },
    "impact_video" : {
        "name" : "impact_video",
        "description" : "Creates a video clip with Impact font overlain.",
        "options" : [
            create_option(
                name="link",
                description="The YouTube video link or id to use.",
                option_type=OptionType.STRING,
                required=True
            ),
            create_option(
                name="top_text",
                description="Text to put on the top. (Automatically capitalized.)",
                option_type=OptionType.STRING,
                required=True
            ),
            create_option(
                name="bottom_text",
                description="Text to put on the bottom. (Automatically capitalized.)",
                option_type=OptionType.STRING,
                required=True
            ),
            create_option(
                name="clip_start",
                description="The time (in seconds) signifying the start of the clip.",
                option_type=OptionType.INTEGER,
                required=True
            ),
            create_option(
                name="clip_end",
                description="The time (in seconds) signifying the end of the clip.",
                option_type=OptionType.INTEGER,
                required=True
            )
        ]
    },
    "audioji_add" : {
        "name" : "add",
        "description" : "Adds a new audioji to the list of available audiojis.",
        "options" : [
            create_option(
                name="name",
                description="The name of the audioji you are creating. This is case-sensitive.",
                option_type=OptionType.STRING,
                required=True
            ),
            create_option(
                name="link",
                description="The YouTube video link or id to grab the audio from.",
                option_type=OptionType.STRING,
                required=True
            ),
            create_option(
                name="clip_start",
                description="The time (in seconds) signifying the start of the clip.",
                option_type=OptionType.INTEGER,
                required=True
            ),
            create_option(
                name="clip_end",
                description="The time (in seconds) signifying the end of the clip.",
                option_type=OptionType.INTEGER,
                required=True
            )
        ]
    },
    "audioji_play" : {
        "name" : "play",
        "description" : "Plays an audioji.",
        "options" : [   # TODO: Should give choices for the audiojis currently available for the server
            create_option(
                name="name",
                description="The name of the audioji to play. This is case-sensitive.",
                option_type=OptionType.STRING,
                required=True
            )
        ]
    },
    "audioji_list" : {
        "name" : "list",
        "description" : "Lists all audiojis.",
        "options" : []
    },
    "audioji_info" : {
        "name" : "info",
        "description" : "Shows the metadata for an audioji.",
        "options" : [
            create_option(
                name="name",
                description="The audioji from which to show metadata. This is case-sensitive.",
                option_type=OptionType.STRING,
                required=True
            )
        ]
    },
    "word_occurrences" : {
        "name" : "word_occurrences",
        "description" : "Gives the amount of times a word occurs in a channel by a "
            + "user.",
        "options" : [
            create_option(
                name="user",
                description="The user from whom to count word occurrences.",
                option_type=OptionType.USER,
                required=True
            ),
            create_option(
                name="word",
                description="The word for which to search.",
                option_type=OptionType.STRING,
                required=True
            ),
            create_option(
                name="channel",
                description="The channel from which to search. Defaults to the "
                    + "current channel.",
                option_type=OptionType.CHANNEL,
                required=False
            ),
            create_option(
                name="limit",
                description="The amount of posts from which to choose (per "
                    + "channel). Default is 1000.",
                option_type=OptionType.INTEGER,
                required=False
            )
        ]
    }
}

# Formats the usagetext for a command (in the decorator, not the helptext)
# e.g. "[name] [link] [clipStart] [clipEnd] " (from !audioji add)
def formatUsage(command):
    string = ""
    for arg in help[command]["options"]:
        string += f"[{arg['name']}] "
    return string

# Formats the long helptext for a command
def formatHelptext(command):
    string = "Arguments:"

    # Add argument descriptions ("tabbed" in with two spaces)
    for arg in help[command]["options"]:
        string += f"\n  {arg['name']} ({arg['type']}): {arg['desc']}"
        try: # Add optional text, if possible
            if arg["optional"]:
                string += " (Optional)"
        except: pass

    # Add nota bene if it exists
    try:
        string += f"\n\nNB: {help[command]['nb']}"
    except: pass

    string += "\n\u200c"
    # The indents break if we don't have a character non-indented on the last
    # line, so we'll use the character ZERO WIDTH NON-JOINER to make a line

    # by the way this is the most fucking stupid shit i've ever seen

    return string
