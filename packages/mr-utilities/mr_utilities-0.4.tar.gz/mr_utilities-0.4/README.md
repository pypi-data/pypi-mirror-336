# MR Utilities

This package is used in different chapters of the Jupyter Books related to data analysis.

## Create source distribution

1. Navigate to the project directory (`mr_utilities`).
2. Run the following command to create the source distribution:

   ```bash
   python setup.py sdist
   ```

3. The generated `.tar.gz` file will be located in the `dist` directory.

## Install the Package Locally

You can install the package from the source distribution file on your local machine. Navigate to the directory containing the .tar.gz file and run:

`pip install dist/mr_utilities-0.1.tar.gz`

## Distribute the Package

You can share the .tar.gz file with others. They can install it using the same pip install command mentioned above.


## Upload to PyPI

If you want to make your package publicly available, you can upload it to the Python Package Index (PyPI). To do this, you will need to:

Install twine if you haven't already:

`pip install twine`

Upload your package using twine:

`twine upload dist/*`

This command will prompt you for your PyPI username and password.

## Usage  

```python  
from mr_utilities.grades.grade_utility import load_grade_data
```