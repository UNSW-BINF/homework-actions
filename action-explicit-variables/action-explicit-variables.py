# Autograder core
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


def const_structured_check(astnode) -> bool:
    if isinstance(astnode, (ast.Constant, ast.Num, ast.Str)):
        return True

    if isinstance(astnode, ast.UnaryOp) and isinstance(astnode.op, ast.USub):
        return isinstance(astnode.operand, (ast.Constant, ast.Num)) and isinstance(astnode.operand.n, int)

    if isinstance(astnode, (ast.List, ast.Set, ast.Tuple)):
        return all(const_structured_check(elt) for elt in astnode.elts)

    if isinstance(astnode, ast.Dict):
        return all(const_structured_check(key) and const_structured_check(value)
                   for key, value in zip(astnode.keys, astnode.values))

    return False


def validate_constants(asttree, mandatory_constants) -> tuple[bool, list[str]]:
    constants_map: dict[str, tuple[bool, int]] = {}
    for node in ast.walk(asttree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in mandatory_constants:
                    # If the variable already exists we check if it occurred at a line number before
                    # the current occurrence. If yes then we update the map.
                    _, lineno = constants_map.get(target.id, (True, -1))
                    if target.lineno > lineno:
                        constants_map[target.id] = (
                            const_structured_check(node.value),
                            target.lineno
                        )

    return [var_name for var_name, (is_constant, _) in constants_map.items() if not is_constant]


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
    invalid_constants = []

    # Parse the code into an AST
    try:
        code_ast = ast.parse(notebook_code)
        code_ast_error = None

        mandatory_variables = sys.argv[1:]
        invalid_constants = validate_constants(code_ast, mandatory_variables)

    except Exception:
        code_ast = None
        code_ast_error = traceback.format_exc()

    return (
        code_ast != None and not invalid_constants,
        code_ast_error,
        invalid_constants
    )


def get_notebook_filename(filenames) -> str:

    pattern = r"^homework-[1-5]\.ipynb$"
    notebook_files = [fn for fn in filenames if re.match(pattern, fn)]

    if len(notebook_files) == 1:
        return notebook_files[0]

    elif len(notebook_files) > 1:
        raise KeyError(
            f"Too many homework notebooks detected: {notebook_files}. Please delete or rename one."
        )

    else:
        raise KeyError(
            "No homework notebook detected. Check the name of the homework notebook and keep the original name."
        )


if __name__ == "__main__":

    DIR = "./"
    NOTEBOOK = get_notebook_filename(os.listdir(DIR))

    print("Checking variables: ", sys.argv[1:])

    success, error_code, invalid_constants = parse_ast(NOTEBOOK, directory=DIR)

    if success:
        print("Syntax check successful.")

    elif invalid_constants:
        raise ValueError(
            f"Invalid constants: {', '.join(var for var in invalid_constants)}!"
        )

    else:
        raise KeyError(
            f"Your jupyter notebook: {NOTEBOOK}, has a syntax error. Please check your code."
        )
