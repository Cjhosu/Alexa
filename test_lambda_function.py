"""
This is an Alexa skill called drink menu
"""

from __future__ import print_function

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
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
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the pyhton Bytes Dinner"
    reprompt_text = "Welcome to the bytes dinner featuring python, you can ask what do you have to drink" 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def create_chosen_drink_attributes(chosen_drink):
    return {"chosenDrink": chosen_drink}

def list_drinks(intent, session):
    session_attributes = None
    should_end_session = False
    card_title = 'List Drinks'
    speech_output = 'We have beer, wine, water, and soda'
    reprompt_text = "You can say what do you have to drink to get a drink list"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def request_drink_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    if intent ['slots']['drinkName']['resolutions']['resolutionsPerAuthority'][0]['status']['code'] == "ER_SUCCESS_MATCH":
        drink_name = intent['slots']['drinkName']['value']
        session_attributes = create_chosen_drink_attributes(drink_name)
        speech_output = "Great, who is speaking"
        reprompt_text = "You can for a drink by saying may I have a ..."
    else:
        speech_output = "I am not sure what to do with that"
        reprompt_text = "I'm not sure what you'd like to drink"
    return set_guest_from_session(intent, session)

def get_drink_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "chosenDrink" in session.get('attributes', {}):
        chosen_drink = session['attributes']['chosenDrink']
        speech_output = "You've declared you want a " + chosen_drink + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite booze is. " \
                        "You can say, my favorite drink is booze."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def set_guest_from_session(intent, session):
    session_attributes = create_chosen_drink_attributes(drink_name)
    reprompt_text = "Who is speaking again"
    if 'guestName' in intent ['slots']:
        guest_name = intent['slots']['guestName']['value']
        speech_output = "Thanks" + guest_name + "I'll get you a" + drink_name
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):

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
    if intent_name == "RequestDrinkIntent":
        return request_drink_in_session(intent, session)
    elif intent_name == "SearchByDrinkIntent":
        return list_drinks(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.61aac195-4775-4656-94b9-98b9c3b86c32"):
        raise ValueError("Invalid Application ID")
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
