from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='maprdb_python_client',
      version='1.0.18062201',
      description='MapR-DB Python Client',
      url='https://github.com/mapr/maprdb-python-client/',
      author='MapR, Inc.',
      keywords='ojai python client mapr maprdb',
      packages=find_packages(exclude=['test*', 'docs*', 'examples*']),
      install_requires=['aenum>=2.0.10', 'grpcio>=1.9.1', 'grpcio-tools>=1.9.1', 'ojai-python-api>=1.0',
                        'python-dateutil>=2.6.1', 'retrying>=1.3.3'],
      python_requires='==2.7.*',
      long_description=long_description
      )
