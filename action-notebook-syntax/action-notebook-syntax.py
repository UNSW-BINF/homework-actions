import ast
import os
import traceback
import nbconvert
import re
import sys

def remove_ipython_commands(s):
    filtered_string = ""
    for line in s.split("\n"):
        if not line.startswith("get_ipython()"):
            filtered_string += line + "\n"
    return filtered_string

def parse_ast(NOTEBOOK, directory="./"):
    writer = nbconvert.writers.FilesWriter()
    notebook_code, resources = nbconvert.export(
        nbconvert.exporters.PythonExporter,
        os.path.join(directory, NOTEBOOK),
    )
    # Filter out any ipython notebook magic commands
    notebook_code = remove_ipython_commands(notebook_code)

    # Write code to file so manual inspection is easier
    py_file = NOTEBOOK.split(".")[0]
    writer.write(notebook_code, resources, os.path.join(directory, py_file))

    # Parse the code into an AST
    try:
        code_ast = ast.parse(notebook_code)
        code_ast_error = None

    except Exception:
        code_ast = None
        code_ast_error = traceback.format_exc()

    return (
        code_ast != None,
        code_ast_error,
    )


def get_notebook_filename(filenames) -> str:

    pattern = "workbook.ipynb"
    notebook_files = [fn for fn in filenames if re.match(pattern, fn)]
    print(pattern)
    print(notebook_files) 
    print(filenames)
    
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
    NOTEBOOK = get_notebook_filename(os.listdir(DIR))

    success, error_code = parse_ast(NOTEBOOK, directory=DIR)

    if error_code is None:
        print("Syntax check successful.")

    else:
        raise KeyError(
            f"Your jupyter notebook: {NOTEBOOK}, has a syntax error. Please check your code."
        )
