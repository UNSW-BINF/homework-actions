import os
import numpy as np
from PIL import Image

def check_if_image_is_white(image_fn:str) -> bool:

    with Image.open(image_fn) as img:
        np_img = np.array(img)[:, :, :3] # without the brightness
    
    return np.min(np_img) == 255 # all pixels are white

if __name__ == "__main__":

    DIR = "."

    images = [fn for fn in os.listdir(DIR) if fn[-4:] == ".png"]

    image_is_white = {
        fn: check_if_image_is_white(fn)
        for fn in images
    }

    if True in list(image_is_white.values()):

        white_images = [fn for fn, is_white in image_is_white.items() if is_white]
        raise ValueError(f"Some of your images are completely white. Please check: {white_images}")

    else:
        print("None of the images is entirely blank.")
