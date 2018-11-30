### Instruction how to build the package ###

Steps to execute:
1. The Python OJAI client builds with only Python 2.7 or higher. Check your Python version by running:
```python --version```
2. Check that you have installed pip:
```pip -V```
3. Next, install the following libraries, if not already installed.
```pip install twine wheel setuptools```
If you encounter issues installing setuptools, run the following command:
```sudo -H pip install setuptools --upgrade```
4. Make sure that you are in the project root directory:
```ls -l setup.py```
5. Run the following command:
```python setup.py bdist_wheel```
6. Upon completion, the command creates the following directories:
- build
- dist
- maprdb_python_client.egg-info

If you want to add the package you have created locally in your project, copy dist/maprdb_python_client* to your project.
To add the package in your virtual environment, run:
```pip install maprdb_python_client-1.1-py2-none-any.whl```
