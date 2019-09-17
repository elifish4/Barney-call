import os
import phonenumbers
import time
import uuid
import json
import requests
from slackclient import SlackClient
from twilio.rest import TwilioRestClient
from twilio.rest import Client 
from twilio.twiml.voice_response import VoiceResponse, Say
from twilio.twiml.voice_response import Pause, VoiceResponse, Say



# environment variables
BOT_ID = os.environ.get("BOT_ID")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
BOB_TOKEN =  os.environ.get("BOB_TOKEN")
OPS_GENIE_TOKEN =  os.environ.get("OPS_GENIE_TOKEN")

# constants
AT_BOT = "<@" + BOT_ID + ">"
CALL_COMMAND = "call"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

   

def get_user_name_by_email(user_email):
    try:
        response = requests.get(
                            'https://api.opsgenie.com/v2/users/'+user_email,
                            headers={
                                    "Accept": "application/json",
                                    "Content-Type": "Content-Type",
                                    "Authorization": OPS_GENIE_TOKEN    
                                }
                            )
        json_data = json.loads(response.text)
        return json_data.get('data').get('fullName')
    
    except:
        pass
        
def get_spesific_on_call_team(team_name,team_id):
    try:
        response = requests.get(
                            'https://api.opsgenie.com/v2/schedules/'+team_id+'/on-calls',
                            headers={
                                    "Accept": "application/json",
                                    "Content-Type": "Content-Type",
                                    "Authorization": OPS_GENIE_TOKEN    
                                }
                            )
        json_data = json.loads(response.text)
        for k in json_data.get('data').get('onCallParticipants'):
            full_name = get_user_name_by_email(k.get('name'))
            #return "Team " + team_name +" - " + full_name + " " + k.get('name')
            return team_name +" - " + full_name
    except:
        pass

def get_all_teams_id(channel):
    oncall_list = ""
    response = requests.get(
                        'https://api.opsgenie.com/v2/schedules/',
                        headers={
                                "Accept": "application/json",
                                "Content-Type": "Content-Type",
                                "Authorization": OPS_GENIE_TOKEN    
                            }
                        )
    json_data = json.loads(response.text)
    for k in json_data.get('data'):
        response = get_spesific_on_call_team(k.get('name'),k.get('id'))
        slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)

def barney_introduce(channel):
    
    response = "Hi, \n" + \
            "My Name is barney, and i will assist you to reach the requested person. \n" +\
            "all you need to do, is just tag me, use the call command and tag the requested person to make him a call with the meessage as voice. \n" +\
            "for example:\n" +\
            "`@barney-bot call @Eli Fish message_to_send`\n"+\
            "ohh yea, you just need to make sure that he has his phone number on his slack profile, .\n" +\
            "and if not.. don't worry i'll search his number on bob :). \n" +\
            "you can also use:" + \
            "`@barney-bot show-oncall` to show the on call list from opsgenie \n." +\
            "have a great day."

    slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)

def get_phone_from_bob(user_email):
    url = 'https://api.hibob.com/v1/people/{0}'.format(user_email)
    response = requests.get(
                        url,
                        headers={
                                "Accept": "application/json",
                                "Content-Type": "Content-Type",
                                "Authorization": BOB_TOKEN    
                            }
                        )
    json_data = json.loads(response.text)
    if "+972" in json_data["home"]["privatePhone"]:
        phone_number = json_data["home"]["privatePhone"]
    else:        
        phone_number = "+972" + json_data["home"]["privatePhone"][1:]

    return (phone_number)

def get_slack_display_name_by_user_id(user_id):
    user_id = user_id.split(" ")
    user_id = user_id[0]

    print(user_id.split('@')[1].split('>')[0])
    
    user_id = user_id.split('@')
    user_id = user_id[1].split('>')[0]

    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            #print (json.dumps(user))
            if 'id' in user and user.get('id').lower() == user_id.lower():

                return user.get('name')

def get_slack_user_email_by_user_id(user_id):
    user_id = user_id.split(" ")
    user_id = user_id[0]

    print(user_id.split('@')[1].split('>')[0])
    
    user_id = user_id.split('@')
    user_id = user_id[1].split('>')[0]

    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'id' in user and user.get('id').lower() == user_id.lower():
                sub_elements = user.get('profile')
                return sub_elements.get('email')

def get_user_phone_number(user_id):
    """
        Recives@barney-call  call efish test the phone number of the requested user that wants to 
        make a call to him.
        The phone number must be in the user correct field on slack.
    """

    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == user_id:
                sub_elements = user.get('profile')

                print(user.get('name'))
                print(sub_elements.get('phone'))
                return sub_elements.get('phone')


    else:
        print("could not find bot user with the name " + user_id)

def handle_command(command, channel, text):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + \
               CALL_COMMAND + "* command with numbers, delimited by spaces."
    if command.startswith(CALL_COMMAND):
        user_name = get_slack_display_name_by_user_id(command[len(CALL_COMMAND):].strip())
        print(user_name)

        user_email = get_slack_user_email_by_user_id(command[len(CALL_COMMAND):].strip())
        print(user_email)
        
        phone = get_user_phone_number(user_name)
        if len(phone) < 9:
            phone = get_phone_from_bob(user_email)

        #response = call_command(command[len(CALL_COMMAND):].strip(),phone)
        response = call_command(phone, user_name, text)

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def call_command(phone_numbers_list_as_string,user_name, text):
    """
        Validates a string of phone numbers, delimited by spaces, then
        dials everyone into a single call if they are all valid.
    """
    text=text.replace(" ", "%20")

    # generate random ID for this conference call
    conference_name = str(uuid.uuid4())
    # split phone numbers by spaces
    #phone_numbers = phone_numbers_list_as_string.split(" ")
    # make sure at least 1 phone numbers are specified
    phone_numbers = phone_numbers_list_as_string

    #if len(phone_numbers) > 0:
    if phone_numbers:
        # check that phone numbers are in a valid format
        #are_numbers_valid, response = validate_phone_numbers(phone_numbers)
        are_numbers_valid = True
        if are_numbers_valid:
            # all phone numbers are valid, so let's dial them together
            #for phone_number in phone_numbers:
            phone_number = phone_numbers
            print("calling " + user_name + " on phone number " + phone_number + " with message: " + text)

            twilio_client.calls.create(to=phone_number,
                                       from_=TWILIO_NUMBER,
                                       url="https://handler.twilio.com/twiml/EHd019d50f833e5d30ad4023e204723136?name="+ user_name+"&"+ "message=" + text)
            response = "calling: " + phone_numbers_list_as_string


    else:
        response = "the *call* command requires at least 1 phone numbers"
    return response

def validate_phone_numbers(phone_numbers):
    """
        Uses the python-phonenumbers library to make sure each phone number
        is in a valid format.
    """
    print("validate_phone_numbers")
    invalid_response = " is not a valid phone number format. Please " + \
                       "correct the number and retry. No calls have yet " + \
                       "been dialed."
    phone_number="+"

    try:
        validate_phone_number = phonenumbers.parse(phone_number)
        if not phonenumbers.is_valid_number(validate_phone_number):
            return False, phone_number + invalid_response
    except:
        return False, phone_number + invalid_response
    return True, None

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is a firehose of data, so
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            try:
                if output and 'text' in output and "introduce" in output.get('text') and BOT_ID in output.get('text'):
                    barney_introduce(output.get('channel'))
                
                if output and 'text' in output and "show-oncall" in output.get('text') and BOT_ID in output.get('text'):
                    get_all_teams_id(output.get('channel'))

                if output and 'text' in output and AT_BOT in output.get('text') and BOT_ID in output.get('text'):
                    # return text after the @ mention, whitespace removed
                    return output.get('text').split(AT_BOT)[1].strip().lower(), \
                        output.get('channel'), output.get('text').split('>')[2]

            except:
                None

    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("CallBot connected and running!")
        while True:
            command, channel, text = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, text)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

