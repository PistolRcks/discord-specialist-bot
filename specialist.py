from PIL import Image, ImageFont, ImageDraw
import ffmpeg

# Constant declarations
SIZE = (400,400)
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
        newFontSize = (fontSize * (SIZE[0] - BORDER_MARGINS[0])) / topSize[0]
        impact = ImageFont.truetype("impact.ttf", newFontSize)
        topSize = draw.textsize(topText, font=impact)
        print(newFontSize)

    # Do the same for bottom text
    bottomSize = draw.textsize(bottomText, font=impact)
    if bottomSize[0] > SIZE[0] - BORDER_MARGINS[0]*2:
        newFontSize = (fontSize * (SIZE[0] - BORDER_MARGINS[0])) / bottomSize[0]
        impact = ImageFont.truetype("impact.ttf", newFontSize)
        bottomSize = draw.textsize(bottomText, font=impact)
        print(newFontSize)

    draw.text(BORDER_MARGINS, topText, font=impact)
    draw.text((BORDER_MARGINS[0], SIZE[1] - BORDER_MARGINS[1] - bottomSize[1]), bottomText, font=impact)
    image.show() # debugging

    return image.tobytes()

def renderVideo(textOverlay):
    pass # TODO


if __name__ == '__main__':
    topText = input("Input toptext: ")
    bottomText = input("Input bottomtext: ")
    createTextOverlay(topText, bottomText)
