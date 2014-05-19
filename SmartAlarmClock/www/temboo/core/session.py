###############################################################################
#
# temboo.core.session.TembooSession
#
# Class for establishing HTTP access to the Temboo REST API.
#
# Python version 2.6
#
#
# Copyright 2013, Temboo Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
#
###############################################################################


import base64
import httplib
import json
from urllib import urlencode

from temboo.core.exception import TembooError
from temboo.core.exception import TembooHTTPError
from temboo.core.exception import TembooCredentialError
from temboo.core.exception import TembooObjectNotAccessibleError


class TembooSession(object):
    """
    Provides basic facilities for communicating with the Temboo servers.
    """
    
    SESSION_BASE_PATH = '/arcturus-web/api-1.0'
    SOURCE_ID="PythonSDK_1.76"
    
    def __init__(self, organization, appkeyname, appkey, domain='master', base_host='temboolive.com', port="443", secure=True):
        """Construct a new TembooSession
    
        organization -- the organization name you used when
                        signing up for the Temboo account.
        appkeyname   -- the appkey name you use to login to
                        your Temboo account.
        appkey       -- the appkey you use to login to
                        your Temboo account

        Keyword arguments
        (These shouldn't be changed unless you know what you're doing.)
        domain       -- the Temboo domain within your
                        organization (default "master")
        base_host    -- the Temboo server you want to
                        connect to (default "temboolive.com")
        port         -- string or integer indicating the port to
                        connect to base_uri on. This will normally be
                        443 for secure (https) connections. (default "443")
        secure       -- True = use secure (https) connections (default)
                        False = use unsecure (http) connections.

        """
        
        organization = organization.strip()
        domain = domain.strip()
        appkeyname = appkeyname.strip()
        appkey = appkey.strip()
        base_host = base_host.strip()
        port = int(port)
        self._secure = bool(secure)
        if base_host == 'localhost':
            self._host = '{0}:{1}'.format(base_host, str(port))
        else:
            self._host = '{0}.{1}:{2}'.format(organization, base_host, str(port))
        self._session_base_path = TembooSession.SESSION_BASE_PATH
        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-temboo-domain': '{0}/{1}'.format(organization, domain),
            'Authorization':'Basic {0}'.format(base64.b64encode(appkeyname + ':' + appkey))
        }

 

    def _do_request(self, http_method, path, body=None, parameters=None):
        """
        Generic HTTP/S connection method.
        
        """

        full_path = self._session_base_path + path
        
        #If any parameters were given, tack them on to the end of the path.
        if parameters:
            full_path += '?' + urlencode(parameters)

        conn = None
        response = None
        try:
            #TO DO: Rewrite to facilitate connection pooling.
            if self._secure:
                conn = httplib.HTTPSConnection(self._host)
            else:
                conn = httplib.HTTPConnection(self._host)

            try:
                conn.request(http_method, full_path, body, self._headers)
            except:
                raise TembooError('An error occurred connecting to the Temboo server. Verify that your Temboo Account Name is correct, and that you have a functioning network connection')

            response = conn.getresponse()
            body = response.read()
           
            #Any 200-series response means success.
            if 200 <= response.status < 300:
                return json.loads(body)

            #401 errors are appkeyname/appkey errors
            if response.status == 401:
                msg = json.loads(body)['error']
                raise TembooCredentialError(msg)
        
            #404 errors are "object not found" (or permissions errors)
            #NOTE: Malformed URIs can result in a 404, too, but the 
            #body text won't be a JSON string.
            if response.status == 404 and body.startswith("{"):
                msg = json.loads(body)['error']
                raise TembooObjectNotAccessibleError(msg, path)

            #Any response < 200 or >= 300 means an error.
            msg = 'Bad HTTP response code. ({0})'.format(response.status)
            raise TembooHTTPError(msg, response.status, response.reason, body)

        finally:
            if conn is not None:
                conn.close()


    def get_content(self, path, parameters=None):
        """Does a GET request to the server.

        Makes a http GET request to the URI 'path' with optional
        'parameters' (a dict of name/value pairs) in the URI.

        path -- a string containing the resource and object id
                path segments of the URI.
                E.g. /choreos/MyChoreos/DoStuff

        parameters -- an optional dict of name:value entries. (Default = None)

        Returns a dict (the server response body, JSON-decoded.)
        """
        return self._do_request('GET', path, parameters=parameters)

    
    def post(self, path, body, parameters=None):
        """Does a POST request to the server.

        Makes a http POST request to the URI 'path' with 'body' and
        optional 'parameters' (a dict of name/value pairs) in the URI.
        
        path -- a string containing the resource and object id
                path segments of the URI.
                E.g. /choreos/MyChoreos/DoStuff
        
        body -- a string containing the body of the PUT request.
                NOTE: Any base-64 encoding of the body argument must
                be performed by the caller before calling this method.

        parameters -- an optional dict of name:value entries. (Default = None)

        Returns a dict (the server response body, JSON-decoded.)

        """
        return self._do_request('POST', path, body, parameters)


