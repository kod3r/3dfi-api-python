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

from nviso.threedfi.http import nViso3DFIHttpClient
from nviso.threedfi.http import nViso3DFIException, nViso3DFIRequestError

def main():
    # Fill the app_id and app_key with the informations coming from
    # your nViso API subsription
    app_id = 'your_app_id'
    app_key = 'your_app_key'

    # Create a client instance
    nviso_client = nViso3DFIHttpClient(app_id, app_key)

    try:
        # Process an image called test.jpg, staying in the working directory
        # Here we set a session id to send all our requests in the same session (optional)
        # For this first call, the sequence number is 0 (optional)
        response = nviso_client.process_image_file(image_path='test.jpg', app_session='test_session', seq_num=0)

        # Display the response
        print response

        # Process an image using a readable buffer (in this case, a file descriptor,
        # but could be a StringIO for example)
        with open('test.jpg', 'rb') as image_data:
            response = nviso_client.process_image_upload(image_data=image_data, app_session='test_session', seq_num=1)

        print response

        # Process an image using an url
        url = 'http://gamst.co.uk/wp-content/uploads/2010/05/36_morten_gamst_pedersen_face_shot.jpg'
        response = nviso_client.process_image_url(url=url, app_session='test_session', seq_num=2)

        print response
    except nViso3DFIException, e:
        print 'Error in calling API: %s' % str(e)
    except nViso3DFIRequestError, e:
        print 'Error returned by API: %s' % str(e)

if __name__ == '__main__':
    main()