import os
import py_compile

if __name__ == "__main__":

    DIR = "."
    
    assert "helper_functions.py" in os.listdir(DIR), "File 'helper_functions.py' is missing. Make sure there are no typos in the name."

    py_compile.compile("helper_functions.py")