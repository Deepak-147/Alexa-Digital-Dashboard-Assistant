from __future__ import print_function
"""
This basic skill demonstrates how alexa voice enabled service can be used to make an interactive Project status board.
It uses Project information from projects under SHELL DIGITALIZATION TEAM.
It uses AWS Lambda function using python which is scalable compute platform. For the skill to be configurable, without
hard coding again if any new project gets added or previous information gets updated, we are using Amazon S3 service to store a configuration file in json format over the cloud.
The reponses are generated from the configuration file itself.

Since Amazon S3 provides eventual consistency, the updated information may not get updated immediately, but over the time it will become consistent.
"""

"""
Set up a Amazon developer account and a Amazon web services(AWS) account. Usage limits to AWS Lambda compute platform is 1M free requests per month, and usage limits to Amazon S3 is 5 GB of Standard Storage.
"""

"""
Open configuration file stored in Amazon Simple Storage Service or S3 bucket named shelldigitalizationhelpline
"""
import urllib
import json
link = "https://s3.amazonaws.com/newbucket147/config.json" # change this url to the S3 bucket location of your file. And remember to make it public!
data = json.load(urllib.urlopen(link))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """ Uncomment some of the console print statements to debug the errors if any """

    """
    print("HELLO IN SPEECHLET")
    print(title)
    print(output)
    print(reprompt_text)
    print(should_end_session)
    print (data['Projects'])
    print (data['Projects'][0]['Description'])
    """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):

    """ Uncomment some of the console print statements to debug the errors if any """
    """
    print("IN BUILD RESPONSE")
    print(session_attributes)
    print(speechlet_response)
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
# All the functions with names starting with 'session' gives required information from current session. Ex: session_project_launch_information gives information about the project launch from the session.
# All the functions with names starting with 'get' gives required information irrespective of the current session.

def get_welcome_response(): # function to give welcome message
    """ If we wanted to initialize the session to have some attributes we could add those here """

    session_attributes = {}
    card_title = "Welcome"

    """ Initialize the string that holds concatenated project names """
    
    number_of_projects = len(data['Projects'])
    project_string = ""
    for i in range( number_of_projects ):#defines range from 1 to number_of_projects-1
        if(i == 0):
            project_string = project_string + data['Projects'][i]['Name']
        elif(i == (number_of_projects - 1)):
            project_string = project_string + " and " + data['Projects'][i]['Name']
        else:
            project_string = project_string + ", " + data['Projects'][i]['Name']
    speech_output = "Welcome to Shell Digitalization Dashboard Assistant. The current projects are: " + project_string + "."

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me information about projects under Digitalization Team. "

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_goodbye_response(): # function to give session end message

    session_attributes = {}
    card_title = "Goodbye"
    speech_output = "Thanks for trying Shell Digitalization Dashboard Assistant. "\
                    "Have a nice day!!"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""

    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


"""def handle_session_end_request():

    card_title = "Session Ended"
    speech_output = "Thanks for trying Shell Digitalization Status Helpline. "\ 
                    "Have a nice day!! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))
"""

def session_project_manager_information(intent, session): # To get Project Manager information from the current session
    
    #print("HELLO IN session PROJECT Manager information")
    
    session_attributes = {}
    reprompt_text = None
    
    if session.get('attributes', {}) and "project_name" in session.get('attributes', {}):
        project_name = session['attributes']['project_name']
        i = 0
        for item in (data['Projects']):
            if (item['Name'].upper() == project_name.upper()):
                speech_output = "The Project Manager for " + \
                    project_name + " is " + data['Projects'][i]['Manager']
                break
            i = i + 1
        should_end_session = False
    else:
        speech_output = "I'm not sure what you asked!"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))

def session_project_launch_information(intent, session): # To get Project launch information from the current session
    
    #print("HELLO IN session PROJECT launch information")
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "project_name" in session.get('attributes', {}):
        project_name = session['attributes']['project_name']
        i = 0
        for item in (data['Projects']):
            if (item['Name'].upper() == project_name.upper()):
                speech_output = data['Projects'][i]['Launch_information']
                break
            i = i + 1
        should_end_session = False
    else:
        speech_output = "I'm not sure what you asked!"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))        


def session_project_app_value_information(intent, session): # To get Project app value information from the current session
    
    # print("HELLO IN session PROJECT app value information")
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "project_name" in session.get('attributes', {}):
        project_name = session['attributes']['project_name']
        i = 0
        for item in (data['Projects']):
            if (item['Name'].upper() == project_name.upper()):
                speech_output = data['Projects'][i]['App_value']
                break
            i = i + 1
        should_end_session = False
    else:
        speech_output = "I'm not sure what you asked!"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))        

def create_project_name_attributes(project_name): # sets session attribute
    return {"project_name": project_name}


def get_project_information(intent, session): # To get Project description
    # print("HELLO IN GET PROJECT")
    
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'ProjectName' in intent['slots']:
        project_name = intent['slots']['ProjectName']['value']
        session_attributes = create_project_name_attributes(project_name)

    queryname = intent['slots']['ProjectName']['value']
    i = 0
    for item in (data['Projects']):
        if (item['Name'].upper()== queryname.upper()):
            print("inside queryname1")
            speech_output = data['Projects'][i]['Description']
            reprompt_text = ""
            break
        i = i + 1
        speech_output = "Sorry! Currently I do not have information on " + \
            queryname.upper() + ". Please try asking about some other project."
        reprompt_text = ""
        should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_project_manager_information(intent, session): # To get Project Manager information irrespective of current session
    # print("HELLO IN GET PROJECT MANAGER")
    
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'ProjectName' in intent['slots']:
        project_name = intent['slots']['ProjectName']['value']
        session_attributes = create_project_name_attributes(project_name)

    queryname = intent['slots']['ProjectName']['value']
    i = 0
    for item in (data['Projects']):
        print("inside PM")
        if (item['Name'].upper()== queryname.upper()):
            print("inside get_project_manager_info")
            speech_output = "The Project Manager for " + \
                project_name + " is " + data['Projects'][i]['Manager']
            reprompt_text = ""
            break
        i = i + 1
        speech_output = "Sorry! Currently I do not have information on " + \
            queryname.upper() + ". Please try asking about some other project."
        reprompt_text = ""
        should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    
def get_project_launch_information(intent, session): # To get Project Launch information irrespective of current session
    # print("HELLO IN GET PROJECT Launch")
    
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'ProjectName' in intent['slots']:
        project_name = intent['slots']['ProjectName']['value']
        session_attributes = create_project_name_attributes(project_name)

    queryname = intent['slots']['ProjectName']['value']
    i = 0
    for item in (data['Projects']):
        print("inside Project launch")
        if (item['Name'].upper()== queryname.upper()):
            print("inside get_project_launch_info")
            speech_output = data['Projects'][i]['Launch_information']
            reprompt_text = ""
            break
        i = i + 1
        speech_output = "Sorry! Currently I do not have information on " + \
            queryname.upper() + ". Please try asking about some other project."
        reprompt_text = ""
        should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

def get_project_app_value_information(intent, session): # To get Project app value information irrespective of current session
    # print("HELLO IN GET PROJECT app value")
    
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'ProjectName' in intent['slots']:
        project_name = intent['slots']['ProjectName']['value']
        session_attributes = create_project_name_attributes(project_name)

    queryname = intent['slots']['ProjectName']['value']
    i = 0
    for item in (data['Projects']):
        print("inside PM")
        if (item['Name'].upper()== queryname.upper()):
            print("inside get_project_manager_info")
            speech_output = data['Projects'][i]['App_value']
            reprompt_text = ""
            break
        i = i + 1
        speech_output = "Sorry! Currently I do not have information on " + \
            queryname.upper() + ". Please try asking about some other project."
        reprompt_text = ""
        should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

"""def on_session_started(session_started_request, session):
   #Called when the session starts

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
"""

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ProjectDescriptionIntent":
        return get_project_information(intent, session)
    elif intent_name == "ProjectManagerIntent":
        return get_project_manager_information(intent, session)
    elif intent_name == "WhoIsProjectManagerIntent":
        return session_project_manager_information(intent, session)
    elif intent_name == "ProjectLaunchIntent":
        return get_project_launch_information(intent, session)
    elif intent_name == "WhereIsLaunchIntent":
        return session_project_launch_information(intent, session)
    elif intent_name == "AppValueIntent":
        return get_project_app_value_information(intent, session)
    elif intent_name == "WhatIsAppValueIntent":
        return session_project_app_value_information(intent, session)    
    elif intent_name == "WelcomeIntent":
        return get_welcome_response()
    elif intent_name == "ExitIntent":
        return get_goodbye_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

    
"""def on_session_ended(session_ended_request, session):
    # Called when the user ends the session. Is not called when the skill returns should_end_session=true

    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
"""

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """

    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.5b4b26ab-ca08-4e20-b66e-08c26f73ce44"): # provide your skill id inside the quotes, otherwise it will give error
        raise ValueError("Invalid Application ID")

    """if event['session']['new']: # If it is a new session, then call on_session_started
        on_session_started({'requestId': event['request']['requestId']}, event['session'])"""

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    """elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])"""
