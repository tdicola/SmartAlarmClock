# -*- coding: utf-8 -*-

###############################################################################
#
# CreateEvent
# Create a new event in a specified calendar.
#
# Python version 2.6
#
###############################################################################

from temboo.core.choreography import Choreography
from temboo.core.choreography import InputSet
from temboo.core.choreography import ResultSet
from temboo.core.choreography import ChoreographyExecution

import json

class CreateEvent(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the CreateEvent Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        Choreography.__init__(self, temboo_session, '/Library/Google/Calendar/CreateEvent')


    def new_input_set(self):
        return CreateEventInputSet()

    def _make_result_set(self, result, path):
        return CreateEventResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return CreateEventChoreographyExecution(session, exec_id, path)

class CreateEventInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the CreateEvent
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((optional, string) A valid access token retrieved during the OAuth process. This is required unless you provide the ClientID, ClientSecret, and RefreshToken to generate a new access token.)
        """
        InputSet._set_input(self, 'AccessToken', value)
    def set_CalendarID(self, value):
        """
        Set the value of the CalendarID input for this Choreo. ((required, string) The ID for the calendar in which to add the event.)
        """
        InputSet._set_input(self, 'CalendarID', value)
    def set_ClientID(self, value):
        """
        Set the value of the ClientID input for this Choreo. ((conditional, string) The Client ID provided by Google. Required unless providing a valid AccessToken.)
        """
        InputSet._set_input(self, 'ClientID', value)
    def set_ClientSecret(self, value):
        """
        Set the value of the ClientSecret input for this Choreo. ((conditional, string) The Client Secret provided by Google. Required unless providing a valid AccessToken.)
        """
        InputSet._set_input(self, 'ClientSecret', value)
    def set_EndDate(self, value):
        """
        Set the value of the EndDate input for this Choreo. ((required, string) The end date of the event, in the format "2012-04-10".)
        """
        InputSet._set_input(self, 'EndDate', value)
    def set_EndTime(self, value):
        """
        Set the value of the EndTime input for this Choreo. ((required, string) The end time for the event, in the format "10:30:00".)
        """
        InputSet._set_input(self, 'EndTime', value)
    def set_EventDescription(self, value):
        """
        Set the value of the EventDescription input for this Choreo. ((optional, string) A short description of the event.)
        """
        InputSet._set_input(self, 'EventDescription', value)
    def set_EventLocation(self, value):
        """
        Set the value of the EventLocation input for this Choreo. ((optional, string) The location for the new event.)
        """
        InputSet._set_input(self, 'EventLocation', value)
    def set_EventTitle(self, value):
        """
        Set the value of the EventTitle input for this Choreo. ((required, string) The title for the new event.)
        """
        InputSet._set_input(self, 'EventTitle', value)
    def set_RefreshToken(self, value):
        """
        Set the value of the RefreshToken input for this Choreo. ((conditional, string) An OAuth Refresh Token used to generate a new access token when the original token is expired. Required unless providing a valid AccessToken.)
        """
        InputSet._set_input(self, 'RefreshToken', value)
    def set_ResponseFormat(self, value):
        """
        Set the value of the ResponseFormat input for this Choreo. ((optional, string) The format that response should be in. Can be set to xml or json. Defaults to json.)
        """
        InputSet._set_input(self, 'ResponseFormat', value)
    def set_StartDate(self, value):
        """
        Set the value of the StartDate input for this Choreo. ((required, string) The start date of the event, in the format "2012-11-03".)
        """
        InputSet._set_input(self, 'StartDate', value)
    def set_StartTime(self, value):
        """
        Set the value of the StartTime input for this Choreo. ((required, string) The start time for the event, in the format "10:00:00".)
        """
        InputSet._set_input(self, 'StartTime', value)

class CreateEventResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the CreateEvent Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """
    		
    def getJSONFromString(self, str):
        return json.loads(str)
    
    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. (The response from Google. Corresponds to the ResponseFormat input. Defaults to JSON.)
        """
        return self._output.get('Response', None)
    def get_CreateEvent(self):
        """
        Retrieve the value for the "CreateEvent" output from this Choreo execution. (The request template with appropriate inputs passed.)
        """
        return self._output.get('CreateEvent', None)
    def get_TimezoneSetting(self):
        """
        Retrieve the value for the "TimezoneSetting" output from this Choreo execution. ((string) The timezone setting retrieved from the specified calendar.)
        """
        return self._output.get('TimezoneSetting', None)
    def get_NewAccessToken(self):
        """
        Retrieve the value for the "NewAccessToken" output from this Choreo execution. ((string) Contains a new AccessToken when the RefreshToken is provided.)
        """
        return self._output.get('NewAccessToken', None)

class CreateEventChoreographyExecution(ChoreographyExecution):
    
    def _make_result_set(self, response, path):
        return CreateEventResultSet(response, path)
