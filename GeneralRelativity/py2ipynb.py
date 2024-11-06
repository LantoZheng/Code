import os
import nbformat as nbf

# Get the current directory
current_dir = os.getcwd()

# Iterate over all files in the directory
for file_name in os.listdir(current_dir):
    if file_name.endswith(".py"):
        # Read the Python file
        with open(file_name, "r") as py_file:
            code = py_file.read()

        # Create a new notebook
        notebook = nbf.v4.new_notebook()

        # Add a code cell with the Python code
        code_cell = nbf.v4.new_code_cell(code)
        notebook["cells"] = [code_cell]

        # Save the notebook as an .ipynb file
        ipynb_file_name = file_name.replace(".py", ".ipynb")
        with open(ipynb_file_name, "w") as ipynb_file:
            nbf.write(notebook, ipynb_file)