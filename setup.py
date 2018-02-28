from setuptools import setup, find_packages
from codecs import open
from os import path
from pip.req import parse_requirements

here = path.abspath(path.dirname(__file__))
install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]
setup(name='maprdb_python_client',
      version='0.1',
      description='MapR-DB Python Client',
      url='https://github.com/mapr/maprdb-python-client/tree/dev',
      author='MapR inc.',
      authoer_email='dshylov@mapr.com',
      keywords='ojai python client mapr maprdb',
      packages=find_packages(exclude=['test*', 'docs*', 'examples*']),
      install_requires=reqs,
      python_requires='>=2.7'
      )

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
