# Cython Build Helper

`cython-build-helper` is a helper for building Cython projects with flexible file copying and module building.

## Installation

```bash
pip install cython-build-helper
```

## Usage

```python
from cython_build_helper import prepare_build_environment

# List of file patterns to copy to intermediate directory for Cython preprocessing and compilation.
files_to_intermediate = ["resources", "src", "*.py"]
# List of file patterns to copy to output directory.
files_to_output = ["resources", "call_main.py", "requirements.txt"]

ext_modules, build_options = prepare_build_environment(
    files_to_intermediate,
    files_to_output
)

# you can use `ext_modules` and `build_options` to build your project with setuptools.
# For example, you can use `setuptools.setup` to build your project.
setup(
    name="my_project",
    ext_modules=ext_modules,
    options=build_options["options"],
)
```
