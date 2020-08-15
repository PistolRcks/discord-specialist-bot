# Discord bot video rendering module
import math
import os
from PIL import Image, ImageFont, ImageDraw
import ffmpeg
import cv2 # FIXME: Literally just for video metadata, should be using something else

# Constant declarations
SIZE = (720,720)
BORDER_MARGINS = (20,20)


# Creates the text overlay and returns it as bytes
def createTextOverlay(topText, bottomText, fontSize=100):
    image = Image.new("RGBA", SIZE, (0,0,0,0)) # Initialize a new image with a transparent background
    impact = ImageFont.truetype("impact.ttf", fontSize)
    draw = ImageDraw.Draw(image, "RGBA")

    # If you're going to use Impact, of course it has to be in all caps...
    topText = topText.upper()
    bottomText = bottomText.upper()


    # Adjust the size of the font to fit within video
    topSize = draw.textsize(topText, font=impact)
    if topSize[0] > SIZE[0] - BORDER_MARGINS[0]*2:
        # Good ol' algebra and cross-multiplication (basically the ratio between fontsize and textwidth should remain the same)
        newFontSize = math.floor((fontSize * (SIZE[0] - BORDER_MARGINS[0])) / topSize[0])
        impact = ImageFont.truetype("impact.ttf", newFontSize)
        topSize = draw.textsize(topText, font=impact)
        print(newFontSize)

    # Do the same for bottom text
    bottomSize = draw.textsize(bottomText, font=impact)
    if bottomSize[0] > SIZE[0] - BORDER_MARGINS[0]*2:
        newFontSize = math.floor((fontSize * (SIZE[0] - BORDER_MARGINS[0])) / bottomSize[0])
        impact = ImageFont.truetype("impact.ttf", newFontSize)
        topSize = draw.textsize(topText, font=impact)
        bottomSize = draw.textsize(bottomText, font=impact)
        print(newFontSize)

    draw.text((SIZE[0]/2 - topSize[0]/2, BORDER_MARGINS[1]), topText, font=impact)
    draw.text((SIZE[0]/2 - bottomSize[0]/2, SIZE[1] - BORDER_MARGINS[1] - bottomSize[1]), bottomText, font=impact)
    #image.show() # debugging

    return image.tobytes()


def renderWithTextOverlay(videoFP, outputFP, textOverlay, inTime, outTime):
    """ Renders a video with the specified text overlay, within the specified timeframe

    Parameters:
        videoFP (str): String of the filepath which holds the specified video file.
        outputFP (str): String of the filepath to which to write.
        textOverlay (bytes): Raw bytes data of the text overlay to use (should be ccreated with `createTextOverlay()`)
        inTime (float): Point in the video from which to trim (in seconds)
        outTime (float): Point in the video from which to stop trimming (in seconds)

    Returns:
        An error code in the form of an integer.
        0 means success
        1 means invalid time constraints
        2 means file save failure
    """

    # Get metadata
    videoLength = 0 # In seconds
    videoFramerate = 0
    v = cv2.VideoCapture(videoFP)
    videoFrames = v.get(cv2.CAP_PROP_FRAME_COUNT)
    videoFramerate = v.get(cv2.CAP_PROP_FPS)
    videoLength = videoFrames / videoFramerate

    # Catch video length errors
    if inTime < 0 or outTime > videoLength or inTime >= outTime:
        print("Selected parameters exceed video length or are impossible to perform! Stopping.")
        return 1

    # Render the text overlay
    image = Image.frombytes("RGBA", SIZE, textOverlay)
    try:
        image.save("img-tmp.png")
    except:
        print("Image failed to save!")
        return 2

    # Render (also I can't use the nicer looking fluent version because fuck you)
    videoFile = ffmpeg.input(videoFP, ss=inTime, to=outTime)
    overlayFile = ffmpeg.input("img-tmp.png")

    stream = ffmpeg.filter(videoFile, "scale", w=-1, h=SIZE[1])
    stream = ffmpeg.filter(stream, "crop", w=SIZE[0], h=SIZE[1])
    stream = ffmpeg.overlay(stream, overlayFile)

    stream = ffmpeg.output(videoFile.audio, stream, outputFP)
    ffmpeg.run(stream)

    # Cleanup
    os.remove("img-tmp.png")

    return 0


if __name__ == '__main__':
    topText = input("Input toptext: ")
    bottomText = input("Input bottomtext: ")
    inTime = float(input("Input second to start on: "))
    outTime = float(input("Input second to end on: "))

    try: os.remove("specialist_overlain.mp4")
    except: print("No file to remove, so not removing")
    renderWithTextOverlay("specialist.mp4", "specialist_overlain.mp4", \
        createTextOverlay(topText, bottomText), \
        inTime, outTime)
