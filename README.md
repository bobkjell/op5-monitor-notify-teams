# op5-monitor-notify-teams
Send notifications from OP5 Monitor to Microsoft Teams.

![alt text](https://github.com/bobkjell/op5-monitor-notify-teams/blob/main/teams-notification.png "Teams notification example")

## Requirements
* MS Teams Incoming Webhook URL, more info here:
  * https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook
* Python 2.7 or 3.6
* python-requests
<br />

## Install required packages
`yum install python-requests -y`

## Configure OP5 Montor with check_commands for host- and service-notifications
Upload script to: `/opt/plugins/custom/` <br/>

Create two new check_commands for host- & service notifications (insert webhook url in command below) <br/>

`command_name = host-notify-teams` <br />
`command_line = $USER1$/custom/notify_teams.py -w '<webhook-url>' -H '$HOSTNAME$' -ho '$HOSTOUTPUT$' -ha '$HOSTALIAS$' -hs '$HOSTSTATE$' -hi '$HOSTADDRESS$' -n '$NOTIFICATIONTYPE$' -l '$LONGDATETIME$'`
  
`command_name = service-notify-teams` <br />
`command_line = $USER1$/custom/notify_teams.py -w '<webhook-url>' -H '$HOSTNAME$' -ha '$HOSTALIAS$' -hi '$HOSTADDRESS$' -S '$SERVICEDESC$' -so '$SERVICEOUTPUT$' -ss '$SERVICESTATE$' -n '$NOTIFICATIONTYPE$' -l '$LONGDATETIME$'`

<br />

Set the configured check_commands as host- and service-notifications commands on contacts to start receiving notifications. 

![alt text](https://github.com/bobkjell/op5-monitor-notify-teams/blob/main/teams-contacts.png "Teams contacts config")

  
## More info
* Use -d (--debug) flag for troubleshooting.
