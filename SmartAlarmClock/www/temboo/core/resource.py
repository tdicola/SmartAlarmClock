###############################################################################
#
# temboo.core.resource._TembooResource
#
# Parent class for Choreography, _TembooEndpoint, _TembooPreset, and
# _TembooVariable.
#
# Python version 2.6
#
#
# Copyright 2012, Temboo Inc.
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
import abc

class _TembooResource(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, temboo_session, temboo_path):
        """Creates a new instance representing an object in the Temboo vault.

        temboo_session -- must be an instance of TembooSession.
        temboo_path -- a string (or an object that can be converted
                       into a string) that represents this object's
                       location in the Temboo vault. E.g.

                       /Choreos/MyStuff/RunReport
        
        """
        
        self._temboo_session = temboo_session
        self._temboo_path = temboo_path
        if not temboo_path.startswith("/"):
            self._temboo_path = "/" + temboo_path
        else:
            self._temboo_path = temboo_path


    def get_session_path(self):
        """Returns the URI path string to the Temboo resource.

        The URI path is passed to the TembooSession object
        for communicating with the Temboo server. It normally
        consists of the resource path segment and the object
        path.  E.g. "/choreos/Library/myFolder/myChoreo"
        
        """
        return self._get_resource_path() + str(self._temboo_path)


    @abc.abstractmethod
    def _get_resource_path(self):
        """Returns the resource path segment string.
        
        e.g. /choreos
        e.g. /variables
        etc.

        """
        pass

        
    def get_temboo_path(self):
        """Returns this object's location in the Temboo vault.
        
        """
        return self._temboo_path


