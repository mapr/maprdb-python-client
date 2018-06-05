## OJAI Connection string format

The connection string for MapR-DB gRPC Service should be as follows:

`<host>[:<port>][?<options...>]`

Where:
 * host - Hostname of MapR Data Access Gateway service.
 * port - Port of MapR Data Access Gateway service.
 * options - Sequence of connection options in format **optionName=optionValue**. Use **;** as a separator between options.
 
 
#### Available options list:
* **auth=<scheme_name>**
The authentication scheme used for the current connection. Only "basic" is supported in the initial release, which is also the default scheme.
* **user=<username>**
The username for the "basic" authentication scheme.
* **password=<password>**
The password for the "basic" authentication scheme.
* **ssl=true|false**
Indicates whether or not a secure connection using SSL/TLS be established. Default is "true". 
* **sslCA=<path_to_a_PEM_file_containing_CA_certificates>**
Path of a local file containing CA certificates in PEM format. Required if ssl enabled.
* **sslTargetNameOverride=<The_CN_identifies_the_host_name_associated_with_the_certificate>**
Single host name in case of a single-name certificate (e.g. mapr.com) or a wildcard name in case of a wildcard certificate (e.g. *.mapr.com)


##### Connection string example:
* Connection is secure, SSL enabled, username/password authentication enabled.    
    ```localhost:5678?auth=basic;user=mapr;password=mapr;ssl=true;sslCA=/opt/mapr/conf/ssl_truststore.pem;sslTargetNameOverride=node.mapr.com```
* Connection isn't secure, client use insecure channel, username/password authentication enabled.    
    ```localhost:5678?auth=basic;user=mapr;password=mapr;ssl=false```


### Create OJAI connection example:

For creating connection to _data access gateway_ user should pass a connection string to **ConnectionFactory**. 
Simple code example:

```
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory

connection_string = 'localhost:5678?auth=basic;user=mapr;password=mapr;ssl=true;sslCA=/opt/mapr/conf/ssl_truststore.pem;sslTargetNameOverride=node.mapr.com'
connection = ConnectionFactory.get_connection(connection_string)
document_store = connection.create_store('/test-store)
```

More examples how to use MapR-DB Python client you can find [here](https://github.com/mapr-demos/private-ojai-2-examples/tree/master/python)