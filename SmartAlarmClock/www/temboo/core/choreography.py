###############################################################################
#
# temboo.core.choreography.Choreography
# temboo.core.choreography.InputSet
# temboo.coreo.choreography.ResultSet
# temboo.core.choreography.ChoreographyExecution
#
# Interface classes for calling and manipulating choreographies. 
#
# Python version 2.6
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

import datetime
import json
import pprint

from temboo.core.resource import _TembooResource
from temboo.core.util import ExecutionStatus
from temboo.core.session import TembooSession

class Choreography(_TembooResource):


    resource_path = '/choreos'
    

    def __init__(self, temboo_session, temboo_path):
        """ Create a Choreography instance.

        temboo_session -- an instance of TembooSession.
        temboo_path -- a string (or an object that can be converted
                       into a string) that represents the location
                       of this choreo on the Temboo server. For example

                       /Choreos/MyStore/RunReport
        
        """
        _TembooResource.__init__(self, temboo_session, temboo_path)


    def execute_with_results(self, choreo_inputs=None):
        """Runs the choreography and waits for it to complete.
        
        This method will run this choreography with the supplied
        inputs, block while waiting for it to complete,
        and return the results as a dict with keys of
        'output' and 'execution'.
        
        choreo_inputs -- an optional instance of InputSet (default = None)

        Returns a ResultSet instance.

        """
        choreo_inputs = choreo_inputs if choreo_inputs else InputSet()
        body = choreo_inputs.format_inputs();
        params = {"source_id": TembooSession.SOURCE_ID}
        return self._make_result_set(self._temboo_session.post(self.get_session_path(), body, params), self._temboo_path)

    def _make_result_set(self, result, path):
        return ResultSet(result, path)
    
    def execute_async(self, choreo_inputs=None, store_results=False):
        """Runs the choreography asynchronously, without waiting for results.
        
        This method will run this choreography with the supplied
        inputs.  It does not wait for the choreography to complete.
        
        choreo_inputs -- an optional instance of InputSet (default = None)

        store_results -- a boolean that determines whether choreo results
                         are saved for later retrieval or discarded immediately
                         on choreo completion. (default = False)

        Returns a ChoreographyExecution instance that can be used to poll
        for status or get the results when the choreography is complete
        (if store_results is True)

        """
        choreo_inputs = choreo_inputs if choreo_inputs else InputSet()
        body = choreo_inputs.format_inputs();
        params = {'mode': 'async', 'store_results':bool(store_results),
                  "source_id":TembooSession.SOURCE_ID}
        result = self._temboo_session.post(self.get_session_path(), body, params)
        exec_id = result.get('id', None)
        if exec_id:
            return self._make_execution(self._temboo_session, exec_id, self._temboo_path)
        return None
   
    def _make_execution(self, session, exec_id, path):
        return ChoreographyExecution(session, exec_id, path)

    def _get_resource_path(self):
        return Choreography.resource_path


class InputSet(object):
    
    def __init__(self):
        self.inputs = {}
        self.preset_uri = None

    def _set_input(self, name, value):
        """Adds (or replaces) an input variable value in the InputSet

        name -- the name of the input variable.
        value -- the value of the input variable.  If not already a string,
                 will be converted to a string before sending to the server.

        """
        self.inputs[name] = value
   
    def _set_inputs(self, inputs):
        """Adds (or replaces) the names and values passed in to this InputSet

        inputs -- can be a dictionary of name/value pairs
                  or an iterable of key/value pairs as a
                  tuple or other iterable of length two.

        """
        self.inputs.update(inputs)

    def set_credential(self, name):
        """Adds (or replaces) the name of the credential to be used as an input
            to the Choreo execution
        """
        self.preset_uri = name
        
    def format_inputs(self):
        """Formats the JSON body of a choreography execution POST request.

        """
       
        all_inputs ={}
        if self.inputs:
            all_inputs['inputs'] = [{'name':name, 'value':self.inputs[name]} for name in self.inputs]

        if self.preset_uri:
            all_inputs['preset'] = str(self.preset_uri)

        return json.dumps(all_inputs)

class ResultSet(object):
    
    def __init__(self, result, path=None):
        """
        Makes a result set from the JSON result returned
        from a choreo execution.

        result -- may be either a dictionary containing choreo execution
                  results or another ResultSet instance. Giving another
                  ResultSet instance is useful for converting a generic
                  ResultSet returned by ChoreographyExecution.get_results
                  into a choreo-specific result set.

        path -- the temboo path of the choreo that generated these results.
                (ignored if result is a ResultSet)
        
        """
        if isinstance(result, ResultSet):
            self._result = result._result
            self._path = result._path
        else:
            self._result = result
            self._path = path

        self._exec_data = self._result.get("execution", {})
        self._output = self._result.get("output", {})

    @property
    def path(self):
        return self._path

    @property
    def exec_id(self):
        return self._exec_data.get('id', None)

    @property
    def status(self):
        return self._exec_data.get('status', ExecutionStatus.ERROR)

    @property
    def start_time(self):
        return self._exec_data.get('starttime', None)

    @property
    def start_time_UTC(self):
        return self._time_to_UTC(self.start_time)

    @property
    def end_time(self):
        return self._exec_data.get('endtime', None)
    
    @property
    def end_time_UTC(self):
        return self._time_to_UTC(self.end_time)

    @property
    def error_time(self):
        return self._exec_data.get('errortime', None)

    @property
    def error_time_UTC(self):
        return self._time_to_UTC(self.error_time)

    @property
    def last_error(self):
        return self._exec_data.get('lasterror', None)

    @property
    def results(self):
        return self._output

    def _time_to_UTC(self, millis):

        if millis:
            #Server gives us time in milliseconds.
            #We need that as a floating point value in seconds.
            t = float(millis)/1000.0
            return datetime.datetime.utcfromtimestamp(t)
    
        return None

    def __str__(self):
        msg = []
        msg.append("Choreo Execution Results")
        msg.append("Path: " + str(self.path))
        msg.append("Execution ID: " + str(self.exec_id))
        msg.append("Status: " + str(self.status))
        msg.append("Start Time: " + str(self.start_time_UTC) + " UTC")
        msg.append("End Time: " + str(self.end_time_UTC) + " UTC")
        msg.append("Error Time: " + str(self.error_time_UTC) + " UTC")
        msg.append("Last Error: " + str(self.last_error))
        msg.append("Outputs:")
        msg.append(pprint.pformat(self._output, width=1))
        return "\n".join(msg)
    

class ChoreographyExecution(_TembooResource):
    
    resource_path = "/choreo-executions"

    def __init__(self, temboo_session, exec_id, choreo_uri=None):
        """ Create a ChoreographyExecution instance.

        ChoreographyExecution objects are normally created and
        returned by Choreography.execute_async.

        temboo_session -- an instance of TembooSession.
        exec_id -- the execution id of the executing choreo
        
        """
        _TembooResource.__init__(self, temboo_session, exec_id)
        self._result_set = None
        self._status = None
        self.choreo_uri = choreo_uri
        self.exec_id = exec_id

    @property
    def status(self):
        if not self._status or self._status == ExecutionStatus.RUNNING:
            response = self._temboo_session.get_content(self.get_session_path())
            if response:
                exec_info = response['execution']
                self._status = exec_info['status']
        
        return self._status


    def _get_resource_path(self):
        return ChoreographyExecution.resource_path


    @property
    def result_set(self):
        """
        Return result set, if it has been populated yet.
        """
        if self.status != ExecutionStatus.RUNNING and self._result_set is None:
            response = self._temboo_session.get_content(self.get_session_path(), {'view':'outputs'})
            self._result_set = self._make_result_set(response, self._temboo_path)

        return self._result_set

    def _make_result_set(self, response, path):
        return ResultSet(response, path)

    def __str__(self):
        msg = []
        msg.append("Choreo Execution")
        msg.append("Path: " + str(self.choreo_uri))
        msg.append("Execution ID: " + str(self.exec_id))
        msg.append("Status: " + str(self.status))
        return "\n".join(msg)
