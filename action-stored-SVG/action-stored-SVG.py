import os
import sys

def stored_as_PNG(check_required:str, svg_files, png_files):

    if check_required in svg_files:
        return False

    png_names = [fn[:-3] for fn in png_files]    
    if check_required[:-3] in png_names:
        return True
    
    return False

if __name__ == "__main__":
    DIR = "."

    # List all files ending in .svg
    required_files = sys.argv[1:]
    svg_files = [fn for fn in os.listdir(DIR) if fn.lower().endswith('.svg')]
    png_files = [fn for fn in os.listdir(DIR) if fn.lower().endswith('.png')]

    invalid_pngs = [
        fn[:-3] + 'png'
        for fn in required_files
        if stored_as_PNG(fn, svg_files, png_files)
    ]

    if invalid_pngs:
        raise ValueError(f"The following images are stored as PNG instead of SVG: {invalid_pngs}")
    else:
        print("All SVG files are valid.")
