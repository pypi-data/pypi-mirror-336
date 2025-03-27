"""
Cython Build Helper
"""

import glob
import os
import shutil

from Cython.Build import cythonize


def prepare_build_environment(
    files_to_intermediate, files_to_output, output_dir="dist"
):
    """Prepare build environment.

    Args:
        files_to_intermediate (list): List of file patterns to copy to intermediate directory for Cython preprocessing and compilation.
        files_to_output (list): List of file patterns to copy to output directory.
        output_dir (str): Output directory. Defaults to "dist".

    Returns:
        tuple: Tuple of ext_modules and build_options.
    """
    # Define build and intermediate directories
    build_dir = "build"
    intermediate_dir = "intermediate"
    # Remove the build directory if it exists
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    # Remove the intermediate directory if it exists
    if os.path.exists(intermediate_dir):
        shutil.rmtree(intermediate_dir)
    # Create the intermediate directory, ignoring errors if it already exists
    os.makedirs(intermediate_dir, exist_ok=True)

    # Copy specified files or folders to the intermediate directory
    for pattern in files_to_intermediate:
        # Iterate over all items matching the pattern
        for item in glob.glob(pattern):
            # If the item is a file, copy it to the intermediate directory
            if os.path.isfile(item):
                shutil.copy2(item, intermediate_dir)
            # If the item is a directory, copy it recursively to the intermediate directory
            elif os.path.isdir(item):
                shutil.copytree(
                    item,
                    os.path.join(intermediate_dir, os.path.basename(item)),
                    dirs_exist_ok=True,
                )

    # Remove the output directory if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    # Create the output directory
    os.makedirs(output_dir)

    # Initialize a list to store Python files
    python_files = []
    # Walk through the intermediate directory and its subdirectories
    for root, dirs, files in os.walk(intermediate_dir):
        # Iterate over all files in the current directory
        for file in files:
            # If the file is a Python file, add it to the list
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    # Initialize a list to store Cython files
    cython_files = []
    # Iterate over all Python files
    for py_file in python_files:
        # Replace the .py extension with .pyx
        pyx_file = py_file.replace(".py", ".pyx")
        # Copy the Python file to the Cython file
        shutil.copyfile(py_file, pyx_file)
        # Add the Cython file to the list
        cython_files.append(pyx_file)

    # Compile the Cython files into extension modules
    ext_modules = cythonize(cython_files)
    # Set the build options for the extension modules
    build_options = {"build_ext": {"build_lib": output_dir}}

    # Copy specified files or folders to the output directory
    for pattern in files_to_output:
        # Iterate over all items matching the pattern
        for item in glob.glob(pattern):
            # If the item is a file, copy it to the output directory
            if os.path.isfile(item):
                shutil.copy2(item, output_dir)
            # If the item is a directory, copy it recursively to the output directory
            elif os.path.isdir(item):
                shutil.copytree(
                    item,
                    os.path.join(output_dir, os.path.basename(item)),
                    dirs_exist_ok=True,
                )

    return ext_modules, build_options
