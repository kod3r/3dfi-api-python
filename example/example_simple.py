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

#
# Example Simple - Call of URL and Image upload services
#

from nviso.threedfi.http import nViso3DFIHttpClient
from nviso.threedfi.http import nViso3DFIException, nViso3DFIRequestError

def main():
    # Fill the app_id and app_key with the informations coming from
    # your nViso API subsription
    my_app_id       = '__INSERT_YOUR_APP_ID__'
    my_app_key      = '__INSERT_YOUR_APP_KEY__'
    my_app_session  = '__INSERT_YOUR_APP_SESSION__'
    seq_num         = None # None = Autoincrement, otherwise integer

    image_list = [ 'test-small.jpg', 'test-large.jpg' ]
    image_url = 'http://gamst.co.uk/wp-content/uploads/2010/05/36_morten_gamst_pedersen_face_shot.jpg'

    # Create a client instance
    nviso_3dfi = nViso3DFIHttpClient( my_app_id, my_app_key )

    try:

        for current_path in image_list:
            # Process an image by a path found on the local file system
            # Here we set a session id to send all our requests in the same session (optional)
            # Set sequence number (optional)
            response = nviso_3dfi.process_image_path(image_path=current_path, app_session=my_app_session, seq_num=seq_num)
            print response.content

            # Process an image using a readable buffer (in this case, a file descriptor,
            # but could be a StringIO for example)
            with open(current_path, 'rb') as image_data:
                response = nviso_3dfi.process_image_upload(image_data=image_data, app_session=my_app_session, seq_num=seq_num)
            print response.content


        # Process an image using an url
        response = nviso_3dfi.process_image_url(url=image_url, app_session=my_app_session, seq_num=seq_num)
        print response.content

    except nViso3DFIException, e:
        print 'Error in calling API: %s' % str(e)
    except nViso3DFIRequestError, e:
        print 'Error returned by API: %s' % str(e)

if __name__ == '__main__':
    main()