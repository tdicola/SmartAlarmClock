# -*- coding: utf-8 -*-

###############################################################################
#
# InboxFeed
# Allows you to access a read-only Gmail feed that contains a list of unread emails.
#
# Python version 2.6
#
###############################################################################

from temboo.core.choreography import Choreography
from temboo.core.choreography import InputSet
from temboo.core.choreography import ResultSet
from temboo.core.choreography import ChoreographyExecution

import json

class InboxFeed(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the InboxFeed Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        Choreography.__init__(self, temboo_session, '/Library/Google/Gmail/InboxFeed')


    def new_input_set(self):
        return InboxFeedInputSet()

    def _make_result_set(self, result, path):
        return InboxFeedResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return InboxFeedChoreographyExecution(session, exec_id, path)

class InboxFeedInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the InboxFeed
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_Label(self, value):
        """
        Set the value of the Label input for this Choreo. ((optional, string) The name of a Gmail Label to retrieve messages from (e.g., important, starred, sent, junk-e-mail, all).)
        """
        InputSet._set_input(self, 'Label', value)
    def set_Mode(self, value):
        """
        Set the value of the Mode input for this Choreo. ((optional, string) Used when an XPath query is provided. Valid values are "select" or "recursive". Select mode will return the first match of the query. In recursive mode, the XPath query will be applied within a loop.)
        """
        InputSet._set_input(self, 'Mode', value)
    def set_Password(self, value):
        """
        Set the value of the Password input for this Choreo. ((required, password) Your Gmail password.)
        """
        InputSet._set_input(self, 'Password', value)
    def set_ResponseFormat(self, value):
        """
        Set the value of the ResponseFormat input for this Choreo. ((optional, string) The format for the response. Valid values are JSON and XML. This will be ignored when providng an XPath query because results are returned as a string or JSON depending on the Mode specified.)
        """
        InputSet._set_input(self, 'ResponseFormat', value)
    def set_Username(self, value):
        """
        Set the value of the Username input for this Choreo. ((required, string) Your full Google email address e.g., martha.temboo@gmail.com.)
        """
        InputSet._set_input(self, 'Username', value)
    def set_XPath(self, value):
        """
        Set the value of the XPath input for this Choreo. ((optional, string) An XPATH query to run.)
        """
        InputSet._set_input(self, 'XPath', value)

class InboxFeedResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the InboxFeed Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """
    		
    def getJSONFromString(self, str):
        return json.loads(str)
    
    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. (The response from Google. This will contain the data from the Gmail feed, or if the XPath input is provided, it will contain the result of the XPath query.)
        """
        return self._output.get('Response', None)
    def get_FullCount(self):
        """
        Retrieve the value for the "FullCount" output from this Choreo execution. ((integer) The number of unread messages. This is parsed from the Google XML response. Note that when using the Label input to retrieve messages from a particular Gmail label, the full count element may be 0.)
        """
        return self._output.get('FullCount', None)

class InboxFeedChoreographyExecution(ChoreographyExecution):
    
    def _make_result_set(self, response, path):
        return InboxFeedResultSet(response, path)
