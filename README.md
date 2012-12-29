# nViso 3D Facial Imaging Python SDK (v1)

The nViso Developer Platform is a set of APIs that make your application more engaging through capturing real-time emotional feedback and enabling next generation real-time interactivity. For a full list of capabilities please consult the [nViso Developer Platform Portal](https://developer.nviso.net) for more information.

This repository contains the open source Python SDK that allows you to access [nViso Developer Platform](https://developer.nviso.net) from your Python application. In order to use this SDK you will need to have an registered and authorized account from the [nViso Developer Platform Portal](https://developer.nviso.net) and a valid application ID and Key. Except as otherwise noted, the nViso 3D Facial Imaging Python SDK is licensed under the MIT Licence (http://opensource.org/licenses/MIT).

## Installation & Dependencies

Install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a
package manager for Python when inside the current directory.

    $ pip install -e .

Don't have pip installed? Try installing it, by running this from the command
line:

    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

Or, you can [download the source code
(ZIP)](https://github.com/nviso/nviso-3dfi-api-python/archive/master "nviso-3dfi-api-python
source code") for `nviso-3dfi-api-python`, and then run:

    $ python setup.py install

You may need to run the above commands with `sudo`.

### Getting Started

Getting started with the nViso 3D Facial Imaging Python SDK couldn't be easier. Create a `nViso3DFIHttpClient` and you're ready to go. You will find a [sample file](https://github.com/nViso/3dfi-api-python/blob/master/example/example_simple.py) that allows you to get started immediately in the [example folder](https://github.com/nViso/3dfi-api-python/blob/master/example/).

### API Credentials

The `nViso3DFIHttpClient` needs your application ID and key found by logging into the [nViso Developer Platform](https://developer.nviso.net). You can pass these directly to the constructor. Your keys should be kept secret and never shared with anyone!

```python
from nviso.threedfi.http import nViso3DFIHttpClient

my_app_id       = '__INSERT_YOUR_APP_ID__'
my_app_key      = '__INSERT_YOUR_APP_KEY__'
client = nViso3DFIHttpClient(my_app_id, my_app_key)
```

Alternately, a `nViso3DFIHttpClient` constructor without these parameters will look for `NVISO_3DFI_APP_ID` and `NVISO_3DFI_APP_KEY` variables inside the current environment.

We suggest storing your credentials as environment variables. Why? You'll never have to worry about committing your credentials and accidentally posting them somewhere public.

```python
from nviso.threedfi.http import nViso3DFIHttpClient
client = nViso3DFIHttpClient()
```

### Processing an Image by URL

The `nViso3DFIHttpClient` can process a URL locating an image in any standard image format (JPEG, PNG, BMP, etc). It optionally accepts a session id and sequence number used for reporting and ordering results.

```python
from nviso.threedfi.http import nViso3DFIHttpClient

my_app_id       = '__INSERT_YOUR_APP_ID__'
my_app_key      = '__INSERT_YOUR_APP_KEY__'
my_app_session  = '__INSERT_YOUR_APP_SESSION_ID__'
image_url       = '__INSERT_YOUR_URL__'
seq_num  		= '__INSERT_YOUR_SEQUENCE_NUMBER__'

client 			= nViso3DFIHttpClient(my_app_id, my_app_key)

try:
	response = client.process_image_url(url=image_url, app_session=my_app_session, seq_num=seq_num)
    print response.content
except nViso3DFIException, e:
	print 'Error in calling API: %s' % str(e)
except nViso3DFIRequestError, e:
	print 'Error returned by API: %s' % str(e)

```

### Processing an Image by Upload

The `nViso3DFIHttpClient` can process an image stored locally on the computer. The selected file will be uploaded as part of the request. It 
optionally accepts a session id and sequence number used for reporting and ordering results.

```python
from nviso.threedfi.http import nViso3DFIHttpClient

my_app_id       = '__INSERT_YOUR_APP_ID__'
my_app_key      = '__INSERT_YOUR_APP_KEY__'
my_app_session  = '__INSERT_YOUR_APP_SESSION_ID__'
image_path      = '__INSERT_YOUR_IMAGE_PATH__'
seq_num  		= '__INSERT_YOUR_SEQUENCE_NUMBER__'

client 			= nViso3DFIHttpClient(my_app_id, my_app_key)

try:
	with open(image_path, 'rb') as image_data:
        response = client.process_image_upload(image_data=image_data, app_session=my_app_session, seq_num=seq_num)
    print response.content
except nViso3DFIException, e:
	print 'Error in calling API: %s' % str(e)
except nViso3DFIRequestError, e:
	print 'Error returned by API: %s' % str(e)
```

### Response Format

Data returned from the API is output either as a JSON object, Javascript, or XML (depending on the format you choose). 

- `json`: the output will be valid JSON with the mimetype of `application/json`. 
- `jsonp`: the output will be valid HTML with the mimetype of `application/javascript`.
- `eml`: the output will be valid EmotionML with the mimetype of `text/xml`.

For further documentation on the response data model please consult the [nViso Developer Platform Portal](https://developer.nviso.net) for more information.

## Support & Feedback

Please shoot us an email if you have questions or feedback (info@nviso.ch) or open a GitHub issue for bugs and feature requests.
