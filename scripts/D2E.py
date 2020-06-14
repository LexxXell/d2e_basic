#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By Lexx Xell 2019

import socketio
import pickle
import json
import sys

from sys import argv as introductory_parameters
from os import system


profile = {}
properties = {}

sio = socketio.Client()

donations_count = 0


#======================  ***  LOADING BLOCK  ***  ==============================

def load_profile(name):
    try:
        with open('profiles/' + name + '.pkl', 'rb') as f:
            print(f'  -- {name} --')
            return pickle.load(f)
    except:
        print('Profile not found.\n')
        return False

def save_properties():
    global properties
    try:
        with open('cfg/config.pkl', 'wb') as f:
            pickle.dump(properties, f, pickle.HIGHEST_PROTOCOL)
    except:
        print('ERROR: Config file not found')
        sys.exit()

def open_profile_by_input_name():
    profile = False
    count = 0
    while (profile == False):
        profile_name = input("Input your profile name: ")
        profile = load_profile(profile_name)
        if (profile == False):
            print('Try again.\n\n')
        count += 1
        if (count > 2):
            count = 0
            profile = open_base_profile()
    properties['last_profile'] = profile_name
    save_properties()
    return profile

def open_base_profile():
    choice = input("Open Base profile? (Y/n) ")
    print('\n')
    if choice == "Y" or choice == "y":
        return load_profile(properties['base_profile'])
    else:
        print('User refused\n\n')
        return False

def load_properties():
    global profile
    global properties
    global introductory_parameters
    try:
        with open('cfg/config.pkl', 'rb') as f:
            properties = pickle.load(f)
    except:
        print('ERROR: Config file not found')
        sys.exit()
    try:
        start_param = introductory_parameters[1]
    except:
        start_param = False
    if (start_param == "help"): print_help()
    if (start_param == "-lp"): profile = open_last_profile()
    else: profile = open_profile_by_input_name()

def open_last_profile():
    profile = load_profile(properties['last_profile'])
    if (profile == False):
        print(f"\n  *** Can`t find last profile {properties['last_profile']} ***\n\n")
        return open_profile_by_input_name()
    else:
        return profile

#===============================================================================

#=====================  ***  SocketIO BLOCK  ***  ==============================

def start_socketio_client():
    global profile
    socketio_data = {'token':profile['token'],
                     'type': profile['socketio_data_type']}
    sio.connect(profile['socketio_url'])
    sio.emit(profile['socketio_event'], socketio_data)

@sio.event
def connect():
    print(
'''
                    #=============================#
                    #  ***  I'm  connected!  ***  #
                    #=============================#

'''
    )

@sio.event
def disconnect():
        print(
'''
                    #=============================#
                    #  *** I'm DISCONNECTED! ***  #
                    #=============================#

'''
        )

@sio.on('donation')
def on_message(data):
    global donations_count
    global profile
    donations_count += 1
    data_json = json.loads(data)
    amount = data_json[profile['amount_tag']]
    event_data = get_event_information(amount)
    event_plugin = plugin_data = "NO EVENT"
    if event_data != False:
        event_plugin = event_data[0]
        plugin_data = event_data[1]
    print(
f'''

 -- {donations_count} --
================================================================================
                         *** Incoming DONATION ***
________________________________________________________________________________

    Amount: {amount} {data_json['currency']}

    Message:
    {data_json[profile['message_tag']]}
________________________________________________________________________________
    Event plugin: {event_plugin}
    Plugin data: {plugin_data}
================================================================================
'''
    )
    if event_plugin != "NO EVENT":
        try:
            with open('plugins/' + event_plugin + '.py', 'rb') as f:
                system('py plugins/' + event_plugin + f'.py {plugin_data}')
        except:
            print("ERROR: Plugin not found.")



def get_event_information(donation_amount):
    try:
        return profile[donation_amount]
    except:
        return False

#===============================================================================

#=======================  ***  TEXT BLOCK  ***  ================================

def print_header():
    print(
'''
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        +++                                                      +++
        +++               DONATION-TO-EVENT                      +++
        +++               By Lexx Xell 2019                      +++
        +++                   D2E v1.0b                          +++
        +++                                                      +++
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
    )

def print_help():
    help_text = "\n\nHELP\n\n-lp     Load last profile\n\n"
    print(help_text)

#===============================================================================


#MainFrame
if __name__ == "__main__":
    print_header()
    load_properties()
    start_socketio_client()
