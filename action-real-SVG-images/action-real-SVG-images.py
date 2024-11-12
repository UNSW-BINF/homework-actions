import os

def check_if_svg_is_valid(svg_fn: str) -> bool:
    try:
        with open(svg_fn, 'r', encoding='utf-8') as file:
            header = file.read(100).strip()  # Read the first 100 characters
            # Check for typical SVG headers
            if header.startswith('<?xml') or header.startswith('<svg'):
                return True
    except UnicodeDecodeError:
        # If the file cannot be read as text, it's likely not an SVG.
        pass
    return False

if __name__ == "__main__":
    DIR = "."

    # List all files ending in .svg
    svg_files = [fn for fn in os.listdir(DIR) if fn.lower().endswith('.svg')]

    # Check each file
    invalid_svgs = [fn for fn in svg_files if not check_if_svg_is_valid(fn)]

    if invalid_svgs:
        raise ValueError(f"The following SVG files are not valid SVGs or may be renamed PNGs: {invalid_svgs}")
    else:
        print("All SVG files are valid.")
