''' Message Helper Functions '''
# Python Libraries
from time import time
from copy import deepcopy
import uuid

# Project Files
from error import InputError, AccessError
from database import get_data
import helpers  # pylint: disable=import-error

MESSAGE_DATA = {
    "message_id": "",
    "u_id": "",
    "message": "",
    "time_created": 1,
    "reacts" : [],
    "is_pinned" : False
    }

MAX_MESSAGE_LENGTH = 1000

GLOBAL_DATA = get_data()


def find_channel_id(msg_id):
    '''Given msg_id, find channel_id.'''
    for channel in GLOBAL_DATA['channels']:
        for message in channel['messages']:
            if message['message_id'] == msg_id:
                return channel['channel_id']
                
    raise InputError(description='Invalid message ID.')


def send_message_later(token, channel_id, message, message_id, time_sent):
    ''' Message send function with update time_created '''
    for channel in GLOBAL_DATA['channels']:
        if channel['channel_id'] == channel_id:
            message_data_copy = deepcopy(MESSAGE_DATA)

            message_data_copy.update({'message_id': message_id})
            message_data_copy.update({'u_id': helpers.token_to_user(token)})
            message_data_copy.update({'message': message})
            message_data_copy.update({'time_created': time_sent})

            channel['messages'].append(message_data_copy)
            GLOBAL_DATA['n_messages'] += 1


def message_id_generator():
    ''' Generate unique ID. '''
    return uuid.uuid4().int  # pylint: disable=no-member

# Error Checks


def joined_channel_check(channel_list, channel_id):
    ''' Raise AccessError if user has not joined channel. '''
    flag = False
    for channel in channel_list['channels']:
        if channel['channel_id'] == channel_id:
            flag = True
            break
    if not flag:
        raise AccessError(description='User has not joined channel')


def time_valid(time_sent):
    ''' Raise InputError if time_sent is in the past. '''
    print("below is time")
    print(time())
    if time_sent < time():
        raise InputError(description='Time is in the past.')


def react_id_valid(react_id):
    '''Raise error if react_id is not a valid ID for the Slacker. '''
    if react_id != 1:
        raise InputError(description='Invalid react')


def user_already_reacted(user_id, message_id, react_id):
    '''Raise error if the user has already reacted. '''
    for channel in GLOBAL_DATA['channels']:  # pylint: disable=too-many-nested-blocks
        for message in channel['messages']:
            if message['message_id'] == message_id:
                for react in message['reacts']:
                    if react['react_id'] == react_id:
                        for u_id in react['u_ids']:
                            if user_id == u_id:
                                raise InputError(description='User already reacted.')


def no_react(message_id):
    ''' Raise InputError when there is no react. '''
    for channel in GLOBAL_DATA['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id and message['reacts'] == []:
                raise InputError(description='Does not contain active react.')


def pinned_check(message_id, is_pinned):
    ''' Raise InputError if the message is already pinned if
    is_pinned == True. If is_pinned == False, raise error if unpinned. '''
    for channel in GLOBAL_DATA['channels']:
        flag = False
        for message in channel['messages']:
            if message['message_id'] == message_id and message['is_pinned'] == is_pinned:
                flag = True
                break  # from 1st loop
        if flag:
            break  # from 2nd loop and function.
    if not flag:  # if still in the function it means message has not been found.
        raise AccessError(description='Message cannot be pinned/unpinned')


def is_owner(u_id, message_id):
    ''' Raise InputError is user is not an owner. '''
    flag = False
    # Break if user is channel owner.
    for channel in GLOBAL_DATA["channels"]:
        if channel["channel_id"] == find_channel_id(message_id):
            for member in channel["members"]:
                if member["u_id"] == u_id and member["channel_permissions"] == 1:
                    flag = True
                    break
        if flag:
            break

    # Break if user is global owner.
    for user in GLOBAL_DATA['users']:
        if user["u_id"] == u_id and user['global_permissions'] == 1:
            flag = True
            break
    if not flag:  # User did not send message and is not channel or slackr owner.
        raise InputError(description='User is not authorised to pin a message')


def authorised_user_check(u_id, message_id):
    ''' Raise AccessError if user deleting message did not send message
    and is not an owner of channel or slackr. '''
    flag = False
    # Break if user did send.
    for channel in GLOBAL_DATA['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id and message['u_id'] == u_id:
                flag = True
                break  # from first loop
        if flag:
            break  # from second loop

    # Break if user is channel owner.
    for channel in GLOBAL_DATA["channels"]:
        if channel["channel_id"] == find_channel_id(message_id):
            for member in channel["members"]:
                if member["u_id"] == u_id and member["channel_permissions"] == 1:
                    flag = True
                    break
        if flag:
            break

    # Break if user is global owner.
    for user in GLOBAL_DATA['users']:
        if user["u_id"] == u_id and user['global_permissions'] == 1:
            flag = True
            break
    if not flag:  # User did not send message and is not channel or slackr owner.
        raise AccessError(description='User is not authorised to remove a message')


def message_exists_check(message_id):
    ''' Raise InputError if message does not exist. '''
    for channel in GLOBAL_DATA['channels']:
        flag = False
        for message in channel['messages']:
            if message['message_id'] == message_id:
                flag = True
                break  # from 1st loop
        if flag:
            break  # from 2nd loop and function.
    if not flag:  # if still in the function it means message has not been found.
        raise AccessError(description='Message does not exist')

