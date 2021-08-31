''' Message tests. '''
''' Written by Richard Zhang, z5118085, March 2020. '''

import pytest
import message
from database import get_data
from workspace_admin import workspace_reset
from auth import auth_register
from channels import channels_create
from channel import channel_join
from error import InputError, AccessError


global_data = get_data()
channel_list = global_data['channels']

# message_send tests


def test_send_admin_success():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    channel1 = channels_create(login1['token'], "Public Channel 2", True)
    channel_join(login1['token'], channel1['channel_id'])

    message.message_send(login1['token'], channel1['channel_id'], "I'm Max Verstappen boys.")
    message_list = channel_list[0]['messages']

    assert message_list[0]["message"] == "I'm Max Verstappen boys."


def test_send_user_success():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login2 = auth_register("conormcgregor@gmail.com", "We'reHereToTakeOver", "Conor", "McGregor")

    channel1 = channels_create(login1['token'], "Public Channel 1", True)
    channel_join(login2['token'], channel1['channel_id'])

    message.message_send(login2['token'], channel1['channel_id'], "The Notorious")
    message_list = channel_list[0]['messages']

    assert message_list[0]["message"] == "The Notorious"


def test_send_message_too_long():
    workspace_reset()
    login1 = auth_register("richard.zhang@gmail.com", "EatSleepCodeRepeat", "Richard", "Zhang")
    channel = channels_create(login1['token'], "Public Channel 3", True)

    with pytest.raises(InputError) as e:
        message.message_send(login1['token'], channel['channel_id'], "yeah bo" + "i" * 1001)


def test_send_user_not_joined_channel():
    workspace_reset()
    login1 = auth_register("conormcgregor@gmail.com", "We'reHereToTakeOver", "Conor", "McGregor")
    login2 = auth_register("richard.zhang@gmail.com", "EatSleepCodeRepeat", "Richard", "Zhang")

    channel = channels_create(login1['token'], "Public Channel 4", True)

    with pytest.raises(AccessError) as e:
        message.message_send(login2['token'], channel['channel_id'], "Coding is my life")

# message_remove tests


def test_admin_remove_success():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login2 = auth_register("conormcgregor@gmail.com", "We'reHereToTakeOver", "Conor", "McGregor")

    channel1 = channels_create(login1['token'], "Public Channel 5", True)
    channel_join(login2['token'], channel1['channel_id'])

    message1 = message.message_send(login2['token'], channel1['channel_id'], "I'm Conor McGregor boys.")
    message2 = message.message_send(login1['token'], channel1['channel_id'], "I'm Max Verstappen boys.")

    message.message_remove(login1['token'], message1['message_id'])
    message.message_remove(login1['token'], message2['message_id'])

    message_list = channel_list[0]['messages']

    assert message_list == []


def test_user_remove_success():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login2 = auth_register("conormcgregor@gmail.com", "We'reHereToTakeOver", "Conor", "McGregor")

    channel1 = channels_create(login1['token'], "Public Channel 6", True)
    channel_join(login2['token'], channel1['channel_id'])

    message1 = message.message_send(login2['token'], channel1['channel_id'], "I'm Conor McGregor boys.")

    message.message_remove(login2['token'], message1['message_id'])

    message_list = channel_list[0]['messages']

    assert message_list == []


def test_remove_invalid_id():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    channel1 = channels_create(login1['token'], "Public Channel 7", True)

    message1 = message.message_send(login1['token'], channel1['channel_id'], "I'm Max Verstappen boys.")

    with pytest.raises(InputError) as e:
        message.message_remove(login1['token'], "InvalidID")


def test_remove_user_not_in_channel():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login2 = auth_register("richard.zhang@gmail.com", "ilovecoding", "Richard", "Zhang")
    login3 = auth_register("conormcgregor@gmail.com", "We'reHereToTakeOver", "Conor", "McGregor")

    channel1 = channels_create(login1['token'], "Public Channel 8", True)
    channel_join(login2['token'], channel1['channel_id'])

    message1 = message.message_send(login2['token'], channel1['channel_id'], "I'm Richard Zhang boys.")

    with pytest.raises(AccessError) as e:
        message.message_remove(login3['token'], message1['message_id'])


def test_remove_unauthorised_user_in_channel():
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login2 = auth_register("richard.zhang@gmail.com", "ilovecoding", "Richard", "Zhang")
    login3 = auth_register("conormcgregor@gmail.com", "We'reHereToTakeOver", "Conor", "McGregor")

    channel1 = channels_create(login1['token'], "Public Channel 9", True)
    channel_join(login2['token'], channel1['channel_id'])
    channel_join(login3['token'], channel1['channel_id'])

    message1 = message.message_send(login2['token'], channel1['channel_id'], "I'm Richard Zhang boys.")

    with pytest.raises(AccessError) as e:
        message.message_remove(login3['token'], message1['message_id'])


# message_edit tests

def test_edit_success_admin():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")

    channel1 = channels_create(login1['token'], "Public Channel 10", True)

    message1 = message.message_send(login1['token'], channel1['channel_id'], "I'm Max Verstappen boys.")

    message.message_edit(login1['token'], message1['message_id'], "This feels good.") 

    message_list = channel_list[0]['messages']

    assert message_list[0]["message"] == "This feels good."


def test_edit_success_authorised_user():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login2 = auth_register("richard.zhang@gmail.com", "ilovecoding", "Richard", "Zhang")

    channel1 = channels_create(login1['token'], "Public Channel 11", True)
    channel_join(login2['token'], channel1['channel_id'])

    message1 = message.message_send(login2['token'], channel1['channel_id'], "I'm Richard boys.")

    message.message_edit(login2['token'], message1['message_id'], "I'm Richard Zhang")

    message_list = channel_list[0]['messages']

    assert message_list[0]["message"] == "I'm Richard Zhang"


def test_edit_success_blank():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login2 = auth_register("richard.zhang@gmail.com", "ilovecoding", "Richard", "Zhang")

    channel1 = channels_create(login1['token'], "Public Channel 11", True)
    channel_join(login2['token'], channel1['channel_id'])

    message1 = message.message_send(login2['token'], channel1['channel_id'], "I'm Richard boys.")

    message.message_edit(login2['token'], message1['message_id'], "")

    message_list = channel_list[0]['messages']

    assert message_list == []


def test_edit_unauthorised_user():
    workspace_reset()
    login1 = auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login2 = auth_register("richard.zhang@gmail.com", "ilovecoding", "Richard", "Zhang")
    login3 = auth_register("yoel.romero@gmail.com", "iluuhyou", "Yoel", "Romero")

    channel1 = channels_create(login1['token'], "Public Channel 12", True)
    channel_join(login2['token'], channel1['channel_id'])
    channel_join(login3['token'], channel1['channel_id'])

    message1 = message.message_send(login2['token'], channel1['channel_id'], "I'm Richard Zhang boys.")

    with pytest.raises(AccessError) as e:
        message.message_edit(login3['token'], message1['message_id'], "I am the soldier of god")
