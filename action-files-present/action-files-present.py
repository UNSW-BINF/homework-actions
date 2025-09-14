# Autograder core
import os
import re

def get_notebook_filename(filenames) -> str:

    pattern = r"workbook\.ipynb$"
    notebook_files = [fn for fn in filenames if re.match(pattern, fn)]

    if len(notebook_files) == 1:
        return notebook_files[0]

    elif len(notebook_files) > 1:
        raise KeyError(
            f"Too many notebooks detected: {notebook_files}. Please delete or rename one."
        )

    else:
        raise KeyError(
            "No notebook detected. Check the name of the notebook and keep the original name."
        )

if __name__ == "__main__":

    DIR = "./"

    notebook_fn = get_notebook_filename(os.listdir(DIR))

    assert "helper_functions.py" in os.listdir(DIR), f"File 'helper_functions.py' is missing. Check for any typos in the filename."
