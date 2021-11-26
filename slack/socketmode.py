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

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.webhook import WebhookClient
from slack_sdk.errors import SlackApiError


app = App(token=secrets.xoxb)


@app.command("/"+secrets.botname+"-hello")
def hello(ack, body):
    user_id = body["user_id"]
    ack(f"Hello, <@{user_id}>!")


@app.command("/"+secrets.botname+"-get-status")
def get_status(ack, body):
    ack()

    # Set up Slack objects
    webhook = WebhookClient(secrets.webhook_url)
    client = WebClient(token=secrets.xoxb)

    # Get status of robot program & if running we'll send details
    # if(htp.check_process_status('Cyberbear_View.exe')):
    if(htp.check_process_status('Cyberbear_View.exe')):

        # Get info to report
        status = 'Running'
        exp_name, pic_names, pic_paths, pic_times = htp.get_exp_info(
            secrets.exp_path)

        # Data we want to include in our update
        message = 'Status : {0}\nExperiment name : {1}\n'.format(
            status, exp_name)

        # Send slack message and check it was successfull
        response = webhook.send(text=message)
        assert response.status_code == 200
        assert response.body == "ok"

        # for each pic in all position dirs this experiment has
        for pic_path in pic_paths:
            # Upload file
            file_name = pic_path
            try:
                result = client.files_upload(
                    channels=secrets.channel_id,
                    file=file_name
                )
            except SlackApiError as e:
                print(e)

    # Else we don't send as many details
    else:
        message = 'Status : Dormant\n'
        # Send slack message and check it was successfull
        response = webhook.send(text=message)
        assert response.status_code == 200
        assert response.body == "ok"


if __name__ == "__main__":
    print('WARNING: Please keep this terminal active or the Slack communication will stop. It\'s okay to minizmie the tab. Thanks.')
    SocketModeHandler(app, secrets.xapp).start()
