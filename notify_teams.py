#!/usr/bin/env python
#
# Description: Send notifications from OP5 Monitor to Microsoft Teams
# Requirements: 
#  * python-requests
#  * Python 2.7 or 3.6
#  * MS Teams webhook URL
#
# "THE BEER-WARE LICENSE" - - - - - - - - - - - - - - - - - -
# This file was initially written by Robert Claesson.
# As long as you retain this notice you can do whatever you
# want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
# - - - - - - - - - - - - - - - robert.claesson@gmail.com - -

# Module import
import requests, argparse, json, logging

# Argument parsing
parser = argparse.ArgumentParser(description='Send notifications from OP5 Monitor to Microsoft Teams.')
parser.add_argument("-H", "--hostname", help="Hostname of alerting host", type=str, required=True)
parser.add_argument("-S", "--service", help="Service description of alerting service", type=str, required=False)
parser.add_argument("-w", "--webhook", help="URL to Teams Webhook", type=str, required=True)
parser.add_argument("-d", "--debug", help="Enable debug to stdout.", action='store_true', required=False)
parser.add_argument("-n", "--notificationtype", help="Notification type", type=str, required=True)
parser.add_argument("-l", "--longdatetime", help="Date/time", type=str, required=True)
parser.add_argument("-ho", "--hostoutput", help="Host alarm message", type=str, required=False)
parser.add_argument("-hs", "--hoststate", help="Host state", type=str, required=False)
parser.add_argument("-ha", "--hostalias", help="Host alias", type=str, required=False)
parser.add_argument("-hi", "--hostipaddress", help="Host IP address", type=str, required=False)
parser.add_argument("-so", "--serviceoutput", help="Service alarm message", type=str, required=False)
parser.add_argument("-ss", "--servicestate", help="Service state", type=str, required=False)
args = parser.parse_args()

# Build service- and host-message
if args.service:
  # Set image and theme color
  if args.servicestate == "CRITICAL":
    imagelink = "https://upload.wikimedia.org/wikipedia/commons/6/62/Icon_Transparent_Error.png"
    themecolor = "FF0000"
  elif args.servicestate == "WARNING":
    imagelink = "https://upload.wikimedia.org/wikipedia/commons/7/73/Icon_Transparent_Warn.png"
    themecolor = "FF9900"
  elif args.servicestate == "OK":
    imagelink = "https://upload.wikimedia.org/wikipedia/commons/b/b0/Icon_Transparent_Green.png"
    themecolor = "36A64F"
  elif args.servicestate == "UNKNOWN":
    imagelink = "https://upload.wikimedia.org/wikipedia/commons/5/56/Icon_Transparent_Question.png"
    themecolor = "6600CC"

  json_body = {
  "@type": "MessageCard",
  "themeColor": themecolor,
  "summary": "ITRS OP5 Monitor Notification",
  "sections": [{
    "activityTitle": args.hostname + "/" + args.service + " is " + args.servicestate,
    "activitySubtitle": "ITRS OP5 Monitor Notification Type: " + args.notificationtype + "\n\nService: " + args.service + "\n\nHost: " + args.hostname + "(" + args.hostalias + ")" + "\n\nAddress: " + args.hostipaddress + "\n\nState: " + args.servicestate + "\n\nDate/Time: " + args.longdatetime + "\n\nPlugin output:\n\n" + args.serviceoutput,
    "activityImage": imagelink}]
  }

else:
  # Set image and theme color
  if args.hoststate == "DOWN":
    imagelink = "https://upload.wikimedia.org/wikipedia/commons/6/62/Icon_Transparent_Error.png"
    themecolor = "FF0000"
  elif args.hoststate == "UP":
    imagelink = "https://upload.wikimedia.org/wikipedia/commons/b/b0/Icon_Transparent_Green.png"
    themecolor = "36A64F"
  elif args.hoststate == "UNREACHABLE":
    imagelink = "https://upload.wikimedia.org/wikipedia/commons/5/56/Icon_Transparent_Question.png"
    themecolor = "6600CC"

  json_body = {
  "@type": "MessageCard",
  "themeColor": themecolor,
  "summary": "ITRS OP5 Monitor Notification",
  "sections": [{
    "activityTitle": args.hostname + " is " + args.hoststate,
    "activitySubtitle": "ITRS OP5 Monitor Notification Type: " + args.notificationtype + "\n\nHost: " + args.hostname + "(" + args.hostalias + ")" + "\n\nAddress: " + args.hostipaddress + "\n\nState: " + args.hoststate + "\n\nDate/Time: " + args.longdatetime + "\n\nPlugin output:\n\n" + args.hostoutput,
    "activityImage": imagelink}]
  }

# Build JSON
json_body = json.dumps(json_body)

# Enable debug log
if args.debug:
  try:
      import http.client as http_client
  except ImportError:
      # Python 2
      import httplib as http_client
  http_client.HTTPConnection.debuglevel = 1
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  requests_log = logging.getLogger("requests.packages.urllib3")
  requests_log.setLevel(logging.DEBUG)
  requests_log.propagate = True

# Send notification to Teams-channel
try:
  headers = {'Content-Type': 'application/json'}
  r = requests.post(args.webhook, data=json_body, headers=headers)
  r.raise_for_status()
except requests.exceptions.HTTPError as error:
  print ("UNKNOWN: " + str(error))
  exit(3)
