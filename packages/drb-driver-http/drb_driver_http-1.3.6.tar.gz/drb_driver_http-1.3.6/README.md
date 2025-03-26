# Http & Https Implementation
This drb-driver-http module implements http and https protocol access with DRB data model.

## Http Factory and Http Node
The module implements the factory model defined in DRB in its node resolver. Based on the python entry point mechanism, this module can be dynamically imported into applications.

The entry point group reference is `drb.driver`.<br/>
The implementation name is `http`.<br/>
The factory class is encoded into `drb.drivers.http`.<br/>
The http signature id is  `b065a5aa-35a3-11ec-8d3d-0242ac130003`<br/>
The https signature id is `c18ef57c-3673-11ec-8d3d-0242ac130003`<br/>

The HttpNode can be instantiated from an uri. The `ParsedPath` class provided in drb core module can help to manage these inputs.

## Using this module
The project is present in https://www.pypi.org service. it can be freely 
loaded into projects with the following command line:

```commandline
pip install drb-driver-http
```
## Access Data
`DrbHttpNode` manages the http protocol to access remote data. The construction
parameter is an url. Both http and https are supported. They allow access the
http content en header. The content is accessible with `value` node class 
attribute. It shall also be possible to retrieve specific streamed 
implementation using `get_impl` methode.
The URL HTTP GET response header of the given URL is accessible via
`attributes` of the node.

```python
from drb.drivers.http import DrbHttpNode

node = DrbHttpNode('https://gitlab.com/drb-python/impl/http/-/raw/main/README.md')

print(node.name)
print(node.attributes)
print(node.path)
print(node.value)
```
HTTP protocol does not allow navigation inside http path so this 
implementation is not able to provide any children of the same HTTP type.
## Authentication
Http node is able to manage Basic authentication based on username and 
password, as well as OAuth2.0 authentication based on token.
It should also support Digest authentication via requests package
`HTTPDigestAuth` implementation.

### Basic Auth
To implements Basic authentication connection, the `HTTPBasicAuth` class
from requests package is used.

```python
from requests.auth import HTTPBasicAuth
from drb.drivers.http import DrbHttpNode

auth = HTTPBasicAuth('username', 'password')
node = DrbHttpNode('https://www.gael.fr', auth=auth)
```

### OAuth2.0 connection
A dedicated `HTTPOAuth2` class is available to manage OAuth2.0 authentication.
It allows token retrieval and refresh when expired.

```python
from drb.drivers.http import DrbHttpNode, HTTPOAuth2

svc_url = 'https://www.gael-systems.com/service'
token_svc = 'https://auth.gael-systems.com/token'
user = 'user'
password = 'pass'
service_id = 'service'
secret = 'secret'

auth = HTTPOAuth2(username=user, password=password, token_url=token_svc,
                  client_id=service_id, client_secret=secret)

node = DrbHttpNode(svc_url, auth=auth)
```

The renewal event of the token is triggered by computation. Based on the 
token expiration delay, the implementation computes the period to create or
refresh a new token. Thanks to this mechanism, no unnecessary connection
is performed by the client for this stage.
## Limitations
None

## Documentation

The documentation of this implementation can be found here https://drb-python.gitlab.io/impl/http