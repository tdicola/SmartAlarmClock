# Smart Alarm Clock 
# Gmail email lookup.
# Copyright 2014 Tony DiCola (tony@tonydicola.com)
# Released under an MIT license (http://opensource.org/licenses/MIT)

import json
import struct
import sys
import time

import dateutil.parser
from temboo.core.session import *
from temboo.Library.Google.Gmail import *


def get_unread(temboo_account, temboo_app, temboo_key, temboo_credentials):
	"""Grab feed of unread emails from Gmail."""
	session = TembooSession(temboo_account, temboo_app, temboo_key)
	choreo = InboxFeed(session)
	inputs = choreo.new_input_set()
	inputs.set_credential(temboo_credentials)
	inputs.set_ResponseFormat('json')
	result = choreo.execute_with_results(inputs)
	return result.get_Response()

def entry_has_keyword(keyword):
	"""Return a function that will filter (i.e. return true) if the provided entry has the given keyword in its title."""
	def filter_function(entry):
		if entry is None:
			return False
		title = entry.get('title')
		if title is None:
			return False
		if entry.get('issued') is None:
			return False
		return title.find(keyword) > -1
	return filter_function

def respond(lastseen):
	"""Print the last seen time (seconds since epoch) as an unsigned long value and quit."""
	print struct.pack('L', lastseen)
	sys.exit(0)

if __name__ == '__main__':
	# Parse parameters from command line.
	if len(sys.argv) != 6:
		# Not enough parameters, quit!
		sys.exit(1)
	temboo_account = sys.argv[1]
	temboo_app = sys.argv[2]
	temboo_key = sys.argv[3]
	temboo_credentials = sys.argv[4]
	keyword = sys.argv[5]
	# Search calendar for events.
	response = get_unread(temboo_account, temboo_app, temboo_key, temboo_credentials)
	# Parse events from response.
	data = json.loads(response)
	if data is None:
		respond(0)
	# Grab the issued date of every entry which has the desired keyword in its title.
	entry = data.get('entry')
	if entry is None:
		respond(0)
	dates = map(lambda e: e.get('issued'), filter(entry_has_keyword(keyword), entry))
	# Parse string to datetime and sort in ascending order.
	dates = sorted(map(dateutil.parser.parse, dates))
	# Stop if no dates were found.
	if len(dates) < 1:
		respond(0)
	# Else return the time (in seconds since epoch) for the most recent date.
	respond(time.mktime(dates[-1].timetuple()))
