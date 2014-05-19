# Smart Alarm Clock 
# Gmail alarm lookup script.
# Copyright 2014 Tony DiCola (tony@tonydicola.com)
# Released under an MIT license (http://opensource.org/licenses/MIT)

from datetime import datetime, timedelta
import json
import struct
import sys

import dateutil.parser
from temboo.core.session import *
from temboo.Library.Google.Calendar import *


def search_events(start_utc, end_utc, temboo_account, temboo_app, temboo_key, temboo_credentials, calendar_id):
	"""Execute the calendar event search choreo on Temboo and return the raw JSON response.
	Start_utc and end_utc values are python dates (in UTC) to limit the search for events."""
	session = TembooSession(temboo_account, temboo_app, temboo_key)
	choreo = SearchEvents(session)
	inputs = choreo.new_input_set()
	inputs.set_credential(temboo_credentials)
	inputs.set_SingleEvent('1')
	inputs.set_MinTime(start_utc.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
	inputs.set_CalendarID(calendar_id)
	inputs.set_OrderBy('startTime')
	inputs.set_MaxTime(end.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
	result = choreo.execute_with_results(inputs)
	return result.get_Response()

def parse_start(event):
	"""Parse the start datetime from the provided calendar event (parsed from JSON).
	Ignores all day events and returns a datetime object with the date (or None if no
	start datetime could be parsed)."""
	start = event.get('start')
	if start is None:
		return None
	if 'date' in start:
		# All day events have 'date' instead of 'dateTime' field.
		return None
	return dateutil.parser.parse(start.get('dateTime'))


if __name__ == '__main__':
	# Parse parameters from command line.
	if len(sys.argv) != 6:
		# Not enough parameters, quit!
		sys.exit(1)
	temboo_account = sys.argv[1]
	temboo_app = sys.argv[2]
	temboo_key = sys.argv[3]
	temboo_credentials = sys.argv[4]
	calendar_id = sys.argv[5]
	# Limit event search to next 24 hours.
	start = datetime.utcnow()
	end = start + timedelta(days=1)
	# Search calendar for events.
	response = search_events(start, end, temboo_account, temboo_app, temboo_key, temboo_credentials, calendar_id)
	# Parse events from search response.
	data = json.loads(response)
	# Print the start time of the earliest non-all day event.
	for event in data.get('items', []):
		start = parse_start(event)
		if start is not None:
			# Found an event with a start time.  Return the hour and minute in a binary format
			# which is easier for the Arduino to parse.
			print struct.pack('BB', start.hour, start.minute)
			sys.exit(0)
