"""
Drew Dahlquist,
University of Missouri - Columbia,
College of Engineering,
Dept. of EECS

DMC Lab

2021
"""

import secrets
import htp

from slack_sdk.webhook import WebhookClient
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def main():

    # Slack setup
    webhook = WebhookClient(secrets.webhook_url)
    client = WebClient(token=secrets.xoxb)

    # Get status of robot
    # If running we'll send details
    if(htp.check_process_status('Cyberbear_View.exe')):
        status = 'Running'

        # Get info to report
        exp_name, pic_names, pic_paths, pic_times = htp.get_exp_info(
            secrets.exp_path)

        # Data we want to include in our update
        message = 'Status : {0}\nExperiment name : {1}\n'.format(
            status, exp_name)

        # Send slack message and check it was successfull
        response = webhook.send(text=message)
        assert response.status_code == 200
        assert response.body == "ok"

        """commenting below code block out since we only wants pics by slash command request"""
        # for each pic in all position dirs this experiment has
        # for pic_path in pic_paths:
        #	# Upload file
        #	file_name = pic_path
        #	try:
        #		result = client.files_upload(
        #			channels=secrets.channel_id,
        #			file=file_name
        #		)
        #	except SlackApiError as e:
        #		print(e)

        htp.set_dormant_count(0)  # update our count of "Dormant" messages

    # Else we don't send as many details
    elif(htp.get_dormant_count() < secrets.max_dormant_msgs):
        message = 'Status : Dormant\n'
        # Send slack message and check it was successfull
        response = webhook.send(text=message)
        assert response.status_code == 200
        assert response.body == "ok"


if __name__ == "__main__":
    main()
