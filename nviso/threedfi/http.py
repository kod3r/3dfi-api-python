#
# Copyright (c) 2012 nViso SA. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#

# Require poster to send mulipart encoded request
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib
import urllib2
import json
register_openers()

class nViso3DFIException(BaseException):
    """Generic nViso 3DFI API Error. All other errors extend this."""
    pass

class nViso3DFIRequestError(nViso3DFIException):
    """Indicates an error during the request. Most likely an error connecting to
    the nViso 3DFI API servers. (HTTP 500 error).
    """
    def __init__(self, status, uri, msg="", code=None):
        self.uri = uri
        self.status = status
        self.msg = msg
        self.code = code

    def __str__(self):
        return "HTTP ERROR %s: %s \n %s" % (self.status, self.msg, self.uri)

class Response(object):
    """
    Take a urllib2 response and turn it into a requests response
    """
    def __init__(self, content, status_code, url):
        self.content = content
        self.status_code = status_code
        self.ok = self.status_code < 400
        self.url = url

class nViso3DFIHttpClient(object):

    # API base path
    API_URL_SECURE         = 'https://3dfi.nviso.net/api/v1/'
    API_URL_STANDARD     = 'http://3dfi.nviso.net/api/v1/'

    def __init__(self, app_id, app_key, api_url=API_URL_SECURE ):
        """
        Initialize the nViso 3DFI api http client.
        :param app_id: The app_id given by your nviso subscription
        :type app_id: string
        :param app_key: The app_key given by your nviso subscription
        :type app_key: string
        :param api_url: The api_url given by your nviso subscription
        :type api_url: string
        """
        self.app_id= app_id
        self.app_key = app_key

        # Services supported by the API
        self.service = {
            'process_image_by_url': api_url + 'process/image/url',
            'process_image_by_upload': api_url + 'process/image/upload'
        }

    def _do_request(self, request, format):
        import xml.dom.minidom as xmldom

        try:
            response = urllib2.urlopen(request)
            status_code = int(resp.status)

            # Format response to create result
            if format=='xml':
                content = xmldom.parseString(response.read())
            else:
                content = json.loads(response.read())

            response.close()

        except urllib2.HTTPError, e:
            raise nViso3DFIException('Failed to send request: %s' % str(e))

        return Response( content, status_code, request.url )

    def process_image_file(self, image_path, app_session=None, seq_num=None):
        """
        Process an image stored in your filesystem.
        :param image_path: The path of the image file
        :type image_path: string
        :param app_session: An optional session id as a string
        :type app_session: string
        :param seq_num: An optional image sequence number
        :type seq_num: int
        :raises: Any exception that "open" function can raise
        """
        image_data = open(image_path,'rb')
        return self.process_image_upload(image_data, app_session, seq_num)

    def process_image_upload(self, image_data, app_session=None, seq_num=None, format='json'):
        """
        Process an image using a "read" compatible buffer (IOString, file descriptor, ...).
        :param image_data: The read compatible buffer containing the image data
        :type image_data: string
        :param app_session: An optional session id as a string
        :type app_session: string
        :param seq_num: An optional image sequence number
        :type seq_num: int
        :param format: The return format for the service.
        :type format: string
        :raises: Any exception that urllib2 can raise
        """

        # Required paramaters
        request_dict = {
            'app_id':self.app_id,
            'app_key':self.app_key,
            'image': image_data
        }

        # Optional paramaters
        if app_session:
            request_dict['app_session'] = app_session
        if seq_num:
             request_dict['seq_number'] = seq_num
        if format:
             request_dict['format'] = format

        # Create the request (POST, multipart encoded)
        datagen, headers = multipart_encode(request_dict)
        request_url = self.service['process_image_by_upload']

        # Execute the request and get the response
        req = urllib2.Request(request_url, datagen, headers)
        resp = self._do_request(req, format)

        # Check if request has an error
        if not resp.ok:
            try:
                error = resp.content
                code = error["code"]
                message = "%s: %s" % (code, error["message"])
            except:
                code = None
                message = resp.content
                raise nViso3DFIRequestError(resp.status_code, resp.url, message, code)

        return resp

    def process_image_url(self, url, app_session=None, seq_num=None, format='jsonp'):
        """
        Process an image using a public accessible url.
        :param url: Url of the image to be processed
        :type url: string
        :param app_session: An optional session id as a string
        :type app_session: string
        :param seq_num: An optional image sequence number
        :type seq_num: int
        :param format: The return format for the service.
        :type format: string
        :raises: Any exception that urllib2 can raise
        """

        # Required paramaters
        request_dict = {
            'app_id':self.app_id,
            'app_key':self.app_key,
            'url': url
        }

        # Optional paramaters
        if app_session:
            request_dict['app_session'] = app_session
        if seq_num:
             request_dict['seq_number'] = seq_num
        if format:
             request_dict['format'] = format

        encoded_params = urllib.urlencode(request_dict)
        request_url = self.service['process_image_by_url']+'?'+encoded_params

        # Execute the request and get the response
        req = urllib2.Request(request_url)
        resp = self._do_request(req, format)

        # Check if request has an error
        if not resp.ok:
            try:
                error = resp.content
                code = error["code"]
                message = "%s: %s" % (code, error["message"])
            except:
                code = None
                message = resp.content
                raise nViso3DFIRequestError(resp.status_code, resp.url, message, code)

        return resp


