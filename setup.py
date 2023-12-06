from setuptools import setup, find_packages


setup(name='maprdb_python_client',
      version='1.1.7',
      description='MapR-DB Python Client',
      url='https://github.com/mapr/maprdb-python-client/',
      author='MapR, Inc.',
      keywords='ojai python client mapr maprdb',
      packages=find_packages(exclude=['test*', 'docs*', 'examples*']),
	  setup_requires=['wheel'],
      install_requires=['aenum>=2.0.10', 'grpcio>=1.9.1', 'grpcio-tools>=1.9.1', 'ojai-python-api>=1.1',
                        'python-dateutil>=2.6.1', 'retrying>=1.3.3', 'future>=0.16.0'],
      python_requires='>=2.7.0',
      long_description='A simple, lightweight library that provides access to MapR-DB.'
                       ' The client library supports all existing OJAI functionality'
                       ' and is absolutely compatible with Java OJAI connector,'
                       ' that runs under the MapR Data Access Gateway.'
      )
