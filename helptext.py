# Discord bot helptext module

help = {
    "smd" : { # Example
        "desc" : "Tells the user to fuck off.", # Description of the command's behavior
        "nb" : "Without a mention, it will tell you to fuck off.", # Additional "nota bene" text to add at the end (optional)
        "args" : [ # Positional arguments (in order of position) in a list
            {
                "name" : "user", # Name of the argument
                "type" : "Username with discriminator, Mention", # Datatype required of the argument
                "desc" : "User to tell to fuck off.", # Description of the argument's use
                "optional" : True # Whether the argument is optional or not (optional, default is False)
            }
        ]
    },
    "impact" : {
        "desc" : "Creates impact font text on a blank background.",
        "nb" : "All text is automatically capitalized.",
        "args" : [
            {
                "name" : "topText",
                "type" : "String",
                "desc" : "Text to put on the top."
            },
            {
                "name" : "bottomText",
                "type" : "String",
                "desc" : "Text to put on the bottom."
            }
        ]
    },
    "specialist" : {
        "desc" : "Creates a video of the P4 protagonist dancing over the song 'specialist' with Impact font text overlain.",
        "args" : [
            {
                "name" : "topText",
                "type" : "String",
                "desc" : "Text to put on the top."
            },
            {
                "name" : "bottomText",
                "type" : "String",
                "desc" : "Text to put on the bottom."
            }
        ]
    },
    "impact_video" : {
        "desc" : "Creates a video clip with Impact font overlain.",
        "args" : [
            {
                "name" : "link",
                "type" : "Youtube Link, Youtube Video ID",
                "desc" : "The Youtube video to use."
            },
            {
                "name" : "topText",
                "type" : "String",
                "desc" : "Text to put on the top."
            },
            {
                "name" : "bottomText",
                "type" : "String",
                "desc" : "Text to put on the bottom."
            },
            {
                "name" : "clipStart",
                "type" : "Float",
                "desc" : "The time (in seconds) signifying the start of the clip."
            },
            {
                "name" : "clipEnd",
                "type" : "Float",
                "desc" : "The time (in seconds) signifying the end of the clip."
            }
        ]
    },
    "audioji_add" : {
        "desc" : "Adds a new audioji to the list of available audiojis.",
        "nb" : "This can also be used to modify existing audiojis.",
        "args" : [
            {
                "name" : "name",
                "type" : "String",
                "desc" : "The name of the audioji you are creating. If you use the name of an existing audioji, it will be overwritten. This is case-sensitive."
            },
            {
                "name" : "link",
                "type" : "Youtube Link, Youtube Video ID",
                "desc" : "The Youtube video to grab the audio from."
            },
            {
                "name" : "clipStart",
                "type" : "Float",
                "desc" : "The time (in seconds) signifying the start of the clip."
            },
            {
                "name" : "clipEnd",
                "type" : "Float",
                "desc" : "The time (in seconds) signifying the end of the clip."
            }
        ]
    },
    "audioji_play" : {
        "desc" : "Plays an audioji.",
        "args" : [
            {
                "name" : "audioji",
                "type" : "Audioji",
                "desc" : "The audioji to play. This is case-sensitive."
            }
        ]
    },
    "audioji_list" : {
        "desc" : "Lists all audiojis.",
        "args" : []
    }
}

# Formats the usagetext for a command (in the decorator, not the helptext)
# e.g. "[name] [link] [clipStart] [clipEnd] " (from !audioji add)
def formatUsage(command):
    string = ""
    for arg in help[command]["args"]:
        string += f"[{arg['name']}] "
    return string

# Formats the long helptext for a command
def formatHelptext(command):
    string = "Arguments:"

    # Add argument descriptions ("tabbed" in with two spaces)
    for arg in help[command]["args"]:
        string += f"\n  {arg['name']} ({arg['type']}): {arg['desc']}"
        try: # Add optional text, if possible
            if arg["optional"]:
                string += " (Optional)"
        except: pass

    # Add nota bene if it exists
    try:
        string += f"\n\nNB: {help[command]['nb']}"
    except: pass

    string += f"\n\u200c" # The indents break if we don't have a character non-indented on the last line, so we'll use the character ZERO WIDTH NON-JOINER to make a line
    # by the way this is the most fucking stupid shit i've ever seen

    return string
