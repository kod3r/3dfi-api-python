# nviso-3dfi-api-python

A module for using the nViso 3D Facial Imaging (3DFI) API.

## Installation

Install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a
package manager for Python when inside the current directory.

    $ pip install -e .

Don't have pip installed? Try installing it, by running this from the command
line:

    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

Or, you can [download the source code
(ZIP)](https://github.com/nviso/nviso-3dfi-api-python/zipball/master "nviso-3dfi-api-python
source code") for `nviso-3dfi-api-python`, and then run:

    $ python setup.py install

You may need to run the above commands with `sudo`.

## Getting Started

Getting started with the nViso 3DFI API couldn't be easier. Create a
`nViso3DFIHttpClient` and you're ready to go.

### API Credentials

The `nViso3DFIHttpClient` needs your nViso 3DFI credentials. You can pass these
directly to the constructor or by environment variables.

```python
from nviso.threedfi.http import nViso3DFIHttpClient

my_app_id       = '__INSERT_YOUR_APP_ID__'
my_app_key      = '__INSERT_YOUR_APP_KEY__'
client = nViso3DFIHttpClient(my_app_id, my_app_key)
```

Alternately, a `nViso3DFIHttpClient` constructor without these parameters will
look for `NVISO_3DFI_APP_ID` and `NVISO_3DFI_APP_KEY` variables inside the
current environment.

We suggest storing your credentials as environment variables. Why? You'll never
have to worry about committing your credentials and accidentally posting them
somewhere public.


```python
from nviso.threedfi.http import nViso3DFIHttpClient
client = nViso3DFIHttpClient()
```
