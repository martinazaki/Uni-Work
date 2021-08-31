''' Message Functions. '''
# Written by Richard Zhang, z5118085, March 2020.

# Python Libraries
from copy import deepcopy
import sched
import time

# Project Files
from database import get_data
from channels import channels_list
import helpers  # pylint: disable=import-error
import message_helpers

MESSAGE_DATA = {
    "message_id": "",
    "u_id": "",
    "message": "",
    "time_created": 1,
    "reacts" : [],
    "is_pinned" : False
    }

REACT_DATA = {
    "react_id": "",
    "u_ids": [],
    "is_this_user_reacted": False,
    }

GLOBAL_DATA = get_data()


def message_send(token, channel_id, message):
    ''' A message_id is generated, message_data is updated with function
    inputs and appended to channel_data. '''
    # Checking for errors.
    helpers.message_length(message)
    message_helpers.joined_channel_check(channels_list(token), channel_id)
    helpers.is_channel(channel_id)

    message_id = message_helpers.message_id_generator()

    for channel in GLOBAL_DATA['channels']: # Loops through channels in database.
        if channel['channel_id'] == channel_id:
            # Make copy to avoid updating previously appended dictionaries.
            message_data_copy = deepcopy(MESSAGE_DATA)

            message_id = float(message_helpers.message_id_generator())

            message_data_copy.update({'message_id': message_id})
            message_data_copy.update({'u_id': helpers.token_to_user(token)})
            message_data_copy.update({'message': message})
            message_data_copy.update({'time_created': time.time()})

            channel['messages'].append(message_data_copy)
            GLOBAL_DATA['n_messages'] += 1

    return {
        'message_id': message_id,
    }


def message_send_later(token, channel_id, message, time_sent):
    '''Send a message to a channel at a specified time in the future. '''
    helpers.is_channel(channel_id)
    helpers.message_length(message)
    message_helpers.time_valid(time_sent)
    message_helpers.joined_channel_check(channels_list(token), channel_id)

    message_id = float(message_helpers.message_id_generator())

    # Set up scheduler
    run_later = sched.scheduler(time.time, time.sleep)
    # Schedule when you want the action to occur
    run_later.enterabs(time_sent, 1, message_helpers.send_message_later,
                       (token, channel_id, message, message_id, time_sent))
    # Block until the action has been run
    run_later.run()

    return {
        'message_id': message_id,
    }


def message_react(token, message_id, react_id):
    ''' Reacts to a valid message. '''

    message_helpers.joined_channel_check(
        channels_list(token),
        message_helpers.find_channel_id(message_id)
    )
    message_helpers.message_exists_check(message_id)
    message_helpers.react_id_valid(react_id)

    message_helpers.user_already_reacted(
        helpers.token_to_user(token),
        message_id,
        react_id
    )

    for channel in GLOBAL_DATA['channels']:  ## pylint: disable=too-many-nested-blocks
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if message['reacts'] == []:  # First react case.
                    react_data_copy = deepcopy(REACT_DATA)

                    react_data_copy.update({'react_id': react_id})
                    react_data_copy['u_ids'].append(helpers.token_to_user(token))

                    # If user reacting is user who sent message.
                    if helpers.token_to_user(token) == message['u_id']:
                        react_data_copy.update({'is_this_user_reacted': True})

                    message['reacts'].append(react_data_copy)

                else:  # Subsequent react requests.
                    for react in message['reacts']:
                        if react['react_id'] == react_id:
                            react['u_ids'].append(helpers.token_to_user(token))

                            if helpers.token_to_user(token) == message['u_id']:
                                react.update({'is_this_user_reacted': True})

    return {}


def message_unreact(token, message_id, react_id):
    ''' Unreacts to a valid message. '''
    message_helpers.joined_channel_check(
        channels_list(token),
        message_helpers.find_channel_id(message_id)
    )
    message_helpers.message_exists_check(message_id)
    message_helpers.react_id_valid(react_id)
    message_helpers.no_react(message_id)

    for channel in GLOBAL_DATA['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                for react in message['reacts']:
                    # If only 1 react, remove react_data dictionary.
                    if react['react_id'] == react_id and len(react['u_ids']) == 1:
                        message['reacts'] = []
                    elif react['react_id'] == react_id:
                        react['u_ids'].remove(helpers.token_to_user(token))

    return {}


def message_pin(token, message_id):
    ''' Pin message if valid. '''
    message_helpers.message_exists_check(message_id)
    message_helpers.is_owner(helpers.token_to_user(token), message_id)
    message_helpers.pinned_check(message_id, False)  # Error if already pinned.
    message_helpers.joined_channel_check(
        channels_list(token),
        message_helpers.find_channel_id(message_id)
    )

    for channel in GLOBAL_DATA['channels']:
        for message_i in channel['messages']:
            if message_i['message_id'] == message_id:
                message_i.update({'is_pinned': True})

    return {}


def message_unpin(token, message_id):
    ''' Unpin message if valid. '''
    message_helpers.message_exists_check(message_id)
    message_helpers.is_owner(helpers.token_to_user(token), message_id)
    message_helpers.pinned_check(message_id, True)  # Error if not pinned.
    message_helpers.joined_channel_check(
        channels_list(token),
        message_helpers.find_channel_id(message_id)
    )

    for channel in GLOBAL_DATA['channels']:
        for message_i in channel['messages']:
            if message_i['message_id'] == message_id:
                message_i.update({'is_pinned': False})

    return {}


def message_remove(token, message_id):
    ''' Removes message if the user is authorised. '''
    helpers.is_channel(message_helpers.find_channel_id(message_id))
    message_helpers.authorised_user_check(helpers.token_to_user(token), message_id)

    for channel in GLOBAL_DATA['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                channel['messages'].remove(message)
                GLOBAL_DATA['n_messages'] -= 1

    return {
    }


def message_edit(token, message_id, message):
    ''' Edits message if the user is authorised. '''
    message_helpers.authorised_user_check(helpers.token_to_user(token), message_id)

    if message == "":
        message_remove(token, message_id)
    else:
        for channel in GLOBAL_DATA['channels']:
            for message_i in channel['messages']:
                if message_i['message_id'] == message_id:
                    message_i.update({'message': message})

    return {
    }

