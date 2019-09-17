# Barney Call Bot
<img src="static/img/Barney.jpeg">


## Purpose
A Slack bot for making phone calls to any phone number using Twilio.

## How to use
Create new tokens for:
- Hibob
- Twilio
- Opsgenie

Create slack bot with the name `barney` and save this bot token.

add env vars as:
> export SLACK_BOT_TOKEN='xxxxxxxxxx'<br>
export BOT_ID='xxxxxx'<br>
export TWILIO_ACCOUNT_SID='xxxxxxxxxxxxxxxx'<br>
export TWILIO_AUTH_TOKEN='xxxxxxxxxxxxxxxx'<br>
export TWILIO_NUMBER='+11111111111'<br>
export BOB_TOKEN='xxxxxxxxxxxxxxxxxxxxxxxxx'<br>
export OPS_GENIE_TOKEN=''GenieKey xxxxxxxxxxxxxx'<br>

## Introduction
Hi <br>
My Name is barney, and i will assist you to reach the requested person.<br>
all you need to do, is just tag me, use the call command and tag the requested person to make him a call with the meessage as voice.<br>

for example:<br>
`@barney call @slackUserName message_to_send`<br>
ohh yea, you just need to make sure that he has his phone number on his slack profile<br>
and if not.. don't worry i'll search his number on bob :). <br>
you can also use:<br>
`@barney show-oncall` to show the on call list from opsgenie.<br>
have a great day.<br>


<br>

###### Copyright
The MIT License (MIT)
Copyright (c) 2019 Eli Fish
<br>
<br>
 Enjoy and have a great day
 <br>
 Eli FIsh
