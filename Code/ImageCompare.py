#TODO:problably this file is pointless
import numpy
from PIL import Image
TEMP_PATH = ".imagecache/"


def get_thumbnail(image, size=(256, 256), stretch_to_fit=False, greyscale=False):
    " get a smaller version of the image - makes comparison much faster/easier"
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size); # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image


#image_similarity_histogram
def compare(filepath1, filepath2):
    from PIL import Image
    import math
    import operator
    from functools import reduce

    if filepath1 != None and filepath2 != None:
        image1 = Image.open(filepath1)
        image2 = Image.open(filepath2)

        image1 = get_thumbnail(image1)
        image2 = get_thumbnail(image2)

        h1 = image1.histogram()
        h2 = image2.histogram()

        rms = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a-b)**2, h1, h2)))/len(h1) )
        return rms
   #TODO:Fix it
    return 99999




