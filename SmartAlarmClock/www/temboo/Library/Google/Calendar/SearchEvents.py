# -*- coding: utf-8 -*-

###############################################################################
#
# SearchEvents
# Allows you to search for events using a variety of search parameters.
#
# Python version 2.6
#
###############################################################################

from temboo.core.choreography import Choreography
from temboo.core.choreography import InputSet
from temboo.core.choreography import ResultSet
from temboo.core.choreography import ChoreographyExecution

import json

class SearchEvents(Choreography):

    def __init__(self, temboo_session):
        """
        Create a new instance of the SearchEvents Choreo. A TembooSession object, containing a valid
        set of Temboo credentials, must be supplied.
        """
        Choreography.__init__(self, temboo_session, '/Library/Google/Calendar/SearchEvents')


    def new_input_set(self):
        return SearchEventsInputSet()

    def _make_result_set(self, result, path):
        return SearchEventsResultSet(result, path)

    def _make_execution(self, session, exec_id, path):
        return SearchEventsChoreographyExecution(session, exec_id, path)

class SearchEventsInputSet(InputSet):
    """
    An InputSet with methods appropriate for specifying the inputs to the SearchEvents
    Choreo. The InputSet object is used to specify input parameters when executing this Choreo.
    """
    def set_AccessToken(self, value):
        """
        Set the value of the AccessToken input for this Choreo. ((optional, string) A valid access token retrieved during the OAuth process. This is required unless you provide the ClientID, ClientSecret, and RefreshToken to generate a new access token.)
        """
        InputSet._set_input(self, 'AccessToken', value)
    def set_CalendarID(self, value):
        """
        Set the value of the CalendarID input for this Choreo. ((required, string) The unique ID for the calendar with the events to retrieve.)
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
    def set_LastModified(self, value):
        """
        Set the value of the LastModified input for this Choreo. ((optional, date) An event's last modification time (as a RFC 3339 timestamp) to filter by.)
        """
        InputSet._set_input(self, 'LastModified', value)
    def set_MaxAttendees(self, value):
        """
        Set the value of the MaxAttendees input for this Choreo. ((optional, integer) The maximum number of attendees to include in the response. If there are more than the specified number of attendees, only the participant is returned.)
        """
        InputSet._set_input(self, 'MaxAttendees', value)
    def set_MaxResults(self, value):
        """
        Set the value of the MaxResults input for this Choreo. ((optional, integer) The maximum number of events to return on one result page.)
        """
        InputSet._set_input(self, 'MaxResults', value)
    def set_MaxTime(self, value):
        """
        Set the value of the MaxTime input for this Choreo. ((optional, date) The max start time to filter by (formatted like 2012-05-22T00:47:43.000Z).)
        """
        InputSet._set_input(self, 'MaxTime', value)
    def set_MinTime(self, value):
        """
        Set the value of the MinTime input for this Choreo. ((optional, date) The minimum start time to filter by (formatted like 2012-05-22T00:47:43.000Z).)
        """
        InputSet._set_input(self, 'MinTime', value)
    def set_OrderBy(self, value):
        """
        Set the value of the OrderBy input for this Choreo. ((optional, string) The order of the events returned in the result. Accepted values are: "startTime" (ordered by start date/time. Must set SingleEvents to 1 to use this) or "updated" (ordered by modification date/time).)
        """
        InputSet._set_input(self, 'OrderBy', value)
    def set_PageToken(self, value):
        """
        Set the value of the PageToken input for this Choreo. ((optional, integer) Indicates which result page to return. Used for paging through results.)
        """
        InputSet._set_input(self, 'PageToken', value)
    def set_Query(self, value):
        """
        Set the value of the Query input for this Choreo. ((optional, string) A keyword search to find events.)
        """
        InputSet._set_input(self, 'Query', value)
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
    def set_ShowDeleted(self, value):
        """
        Set the value of the ShowDeleted input for this Choreo. ((optional, boolean) Whether to include deleted events. Set to 1 (true) to include deleted events. Defaults to 0 (false).)
        """
        InputSet._set_input(self, 'ShowDeleted', value)
    def set_ShowHiddenInvitations(self, value):
        """
        Set the value of the ShowHiddenInvitations input for this Choreo. ((optional, boolean) Whether to include hidden invitations in the result. Set to 1 (true) to enable. The default is 0 (false).)
        """
        InputSet._set_input(self, 'ShowHiddenInvitations', value)
    def set_SingleEvent(self, value):
        """
        Set the value of the SingleEvent input for this Choreo. ((optional, boolean) Whether to expand recurring events into instances and only return single one-off events and instances of recurring events. Defaults to 0 (false).)
        """
        InputSet._set_input(self, 'SingleEvent', value)
    def set_Timezone(self, value):
        """
        Set the value of the Timezone input for this Choreo. ((optional, string) The time zone used in the response (i.e. America/Los_Angeles). The default is the time zone of the calendar.)
        """
        InputSet._set_input(self, 'Timezone', value)

class SearchEventsResultSet(ResultSet):
    """
    A ResultSet with methods tailored to the values returned by the SearchEvents Choreo.
    The ResultSet object is used to retrieve the results of a Choreo execution.
    """
    		
    def getJSONFromString(self, str):
        return json.loads(str)
    
    def get_Response(self):
        """
        Retrieve the value for the "Response" output from this Choreo execution. (The response from Google. Corresponds to the ResponseFormat input. Defaults to JSON.)
        """
        return self._output.get('Response', None)
    def get_NewAccessToken(self):
        """
        Retrieve the value for the "NewAccessToken" output from this Choreo execution. ((string) Contains a new AccessToken when the RefreshToken is provided.)
        """
        return self._output.get('NewAccessToken', None)

class SearchEventsChoreographyExecution(ChoreographyExecution):
    
    def _make_result_set(self, response, path):
        return SearchEventsResultSet(response, path)
