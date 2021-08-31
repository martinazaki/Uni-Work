# drafting a file which stores our data: make lists of dictionaries!


global data

data = {
    "n_users"       : 0,
    "users"         : [],   # this will be a list of dictionaries, each dictionary contains info for one user, user two will have another dictionary, etc. 
    "n_channels"    : 0,
    "channels"      : [],   # also a list of dictionaries. each dictionary contains...the things listed in the sample below
    "n_messages"    : 0 
}

def get_data():
    global data
    return data


'''
Sample data for testing and contents reference


data = {
    "n_users" : 2,
    "users" : [{                                  # each user's information is in a dictionary
        'token': 'valid_token',                   # not sure if I got everything we need, so if you need to add more fields please let everyone know!
        'u_id': 0,
        'email': 'testing@gmail.com',
        'password': 'valid_password',
        'name_first': 'firstname',
        'name_last': 'lastname',
        'handle_str' : 'test_handle',
        'channels': [0],                           # list of channel ids
        'global_permissions':1,   
    },
    {                                  # each user's information is in a dictionary
        'token': 'valid_token1',                   # not sure if I got everything we need, so if you need to add more fields please let everyone know!
        'u_id': 1,
        'email': 'testing1@gmail.com',
        'password': 'valid_password1',
        'name_first': 'firstname1',
        'name_last': 'lastname1',
        'handle_str' : 'test_handle1',
        'channels': [1],                           # list of channel ids
        'global_permissions':2,   
    }],
    "n_channels": 2,
    "channels": [
        {   
        "channel_id": 0, 
        "name": "channel_0", 
        "members": [     
                {
                    'u_id': 0,                    # list of dictionaries, each entry is about one member of the channel
                    'channel_permissions': 1,
                }
            ],
        "messages": [                              # list of dictionaries, each entry contains details about each message sent in that channel
            {   
                 "msg_id": 0,                   # msg_id counts for each message in all channels, msg id is unique to each msg
                 "u_id": 0,
                 "message": "A message",
                 "time_created": 1,             # time_created is an integer (unix timestamp) and also counts for all channels
                 "reacts" : [],
                 "is_pinned" : False
            },
    
            {   
                 "msg_id": 1,
                 "u_id": 0,
                 "message": "Another message",
                 "time_created": 2,
                 "reacts" : [],
                 "is_pinned" : False
            }
    
        ],
        "is_public" : True,  
        "standup" : {                               # Dictionary with only two keys.
            "is_active" : False,
            "time_finish" : None,                    # This stores the time of the stand-up finish if is active and buffers the messages.
            "messages" : []                         # List of messages that follows "messages" structure from channels
            }                                       # All the data will be reseted once the stand-up finishes.
          
        },
        
       {   
       "channel_id": 1,                             # our second test channel
       "name": "channel_1", 
       "members": [     
                {
                    'u_id': 1,
                    'channel_permission': 1,      # 1 means owner, 2 means member, we keep this definition for both global and channel permissions
                }
            ],
        "messages" : [],
        "is_public" : False  
        },
       
    ],
    
    "n_messages" : 2                            # this is for n_messages throughout all channels (total number of messages in the whole slack)
    
}
'''
