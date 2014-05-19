# -*- coding: utf-8 -*-

###############################################################################
#
# GetUnreadMailFromSender
# Allows you to access a read-only Gmail feed that contains a list of unread emails for the specified sender.
#
# Python version 2.6
#
###############################################################################

from temboo.core.choreography import Choreography
from temboo.core.choreography import InputSet
from temboo.core.choreography import ResultSet
from temboo.core.choreography import ChoreographyExecution

import json

class GetUnreadMailFromSender(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the GetUnreadMailFromSender Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        Choreography.__init__(self, temboo_session, '/Library/Google/Gmail/GetUnreadMailFromSender')


    def new_input_set(self):
        return GetUnreadMailFromSenderInputSet()

    def _make_result_set(self, result, path):
        return GetUnreadMailFromSenderResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return GetUnreadMailFromSenderChoreographyExecution(session, exec_id, path)

class GetUnreadMailFromSenderInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the GetUnreadMailFromSender
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_Label(self, value):
        """
        Set the value of the Label input for this Choreo. ((optional, string) The name of a Gmail Label to retrieve messages from (e.g., important, starred, sent, junk-e-mail, all).)
        """
        InputSet._set_input(self, 'Label', value)
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
    def set_SenderEmail(self, value):
        """
        Set the value of the SenderEmail input for this Choreo. ((required, string) Email address of the sender you wish to filter by.)
        """
        InputSet._set_input(self, 'SenderEmail', value)
    def set_Username(self, value):
        """
        Set the value of the Username input for this Choreo. ((required, string) Your full Google email address e.g., martha.temboo@gmail.com.)
        """
        InputSet._set_input(self, 'Username', value)

class GetUnreadMailFromSenderResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the GetUnreadMailFromSender Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """
    		
    def getJSONFromString(self, str):
        return json.loads(str)
    
    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. (The response from Google.)
        """
        return self._output.get('Response', None)
    def get_FullCount(self):
        """
        Retrieve the value for the "FullCount" output from this Choreo execution. ((integer) The number of unread messages. This is parsed from the Google XML response. Note that when using the Label input to retrieve messages from a particular Gmail label, the full count element may be 0.)
        """
        return self._output.get('FullCount', None)

class GetUnreadMailFromSenderChoreographyExecution(ChoreographyExecution):
    
    def _make_result_set(self, response, path):
        return GetUnreadMailFromSenderResultSet(response, path)
