
FROM ubuntu:latest

RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev curl gnupg

MAINTAINER Eli Fish <efish@yotpo.com>

ADD callbot.py /


RUN pip install slackclient
RUN pip install twilio
RUN pip install phonenumbers

ENV SLACK_BOT_TOKEN='XXXXXXXXXXXXXXXXXXXXXXXXXX'
ENV BOT_ID='XXXXXXXXXXXXXXXXXXXX'
ENV TWILIO_ACCOUNT_SID='XXXXXXXXXXXXXXXXXXXXX'
ENV TWILIO_AUTH_TOKEN='XXXXXXXXXXXXXXXXXX'
ENV TWILIO_NUMBER='+11111111'
ENV BOB_TOKEN='XXXXXXXXXXXXXXXXXXXXX'
ENV OPS_GENIE_TOKEN='GenieKey XXXXXXXXXXXXXXXXXx'

CMD [ "python", "./callbot.py" ]





