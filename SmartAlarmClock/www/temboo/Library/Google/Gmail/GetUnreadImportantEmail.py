# -*- coding: utf-8 -*-

###############################################################################
#
# GetUnreadImportantEmail
# Allows you to access a read-only Gmail feed that contains a list of unread emails that are marked important.
#
# Python version 2.6
#
###############################################################################

from temboo.core.choreography import Choreography
from temboo.core.choreography import InputSet
from temboo.core.choreography import ResultSet
from temboo.core.choreography import ChoreographyExecution

import json

class GetUnreadImportantEmail(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the GetUnreadImportantEmail Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        Choreography.__init__(self, temboo_session, '/Library/Google/Gmail/GetUnreadImportantEmail')


    def new_input_set(self):
        return GetUnreadImportantEmailInputSet()

    def _make_result_set(self, result, path):
        return GetUnreadImportantEmailResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return GetUnreadImportantEmailChoreographyExecution(session, exec_id, path)

class GetUnreadImportantEmailInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the GetUnreadImportantEmail
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_Password(self, value):
        """
        Set the value of the Password input for this Choreo. ((required, password) Your Gmail password.)
        """
        InputSet._set_input(self, 'Password', value)
    def set_ResponseMode(self, value):
        """
        Set the value of the ResponseMode input for this Choreo. ((optional, string) Used to simplify the response. Valid values are: simple and verbose. When set to simple, only the message string is returned. Verbose mode returns the full object. Defaults to "simple".)
        """
        InputSet._set_input(self, 'ResponseMode', value)
    def set_Username(self, value):
        """
        Set the value of the Username input for this Choreo. ((required, string) Your full Google email address e.g., martha.temboo@gmail.com.)
        """
        InputSet._set_input(self, 'Username', value)

class GetUnreadImportantEmailResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the GetUnreadImportantEmail Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """
    		
    def getJSONFromString(self, str):
        return json.loads(str)
    
    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. (The response from Google.)
        """
        return self._output.get('Response', None)

class GetUnreadImportantEmailChoreographyExecution(ChoreographyExecution):
    
    def _make_result_set(self, response, path):
        return GetUnreadImportantEmailResultSet(response, path)
