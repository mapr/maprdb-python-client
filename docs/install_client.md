## Install maprdb python client from internal repo ##

1. Now it builds only for python 2.7 or higher. Check your python version
    python --version
2. Check that you have installed pip by running "pip -V".
If you have not installed pip, see https://packaging.python.org/guides/installing-using-linux-tools/.
For example, to install pip on CentOS, run: `sudo yum install python-pip`
3. Create a `pip.conf`. Config file path depends from your OS, you can find instruction [here](https://pip.pypa.io/en/stable/user_guide/#configuration). For centos its `/etc/pip.conf`
4. Modify the `pip.conf` file:
```
[global]
extra-index-url = http://cv:Artifactory4CV!@34.197.167.22/artifactory/api/pypi/pypi-mapr-local/simple
trusted-host = 34.197.167.22
```
!!!! 34.197.167.22 only for CV team? Need to check it !!!!

5. Execute in terminal `pip install maprdb-python-client`

Done.