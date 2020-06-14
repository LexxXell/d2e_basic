#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By LexxXell 2019

import pickle


# Donationalerts token
donationalerts_token = '<token>'



profile = {'token': donationalerts_token,26:['e2k',f'{0xD3} {1}'],'socketio_url': 'wss://socket.donationalerts.ru:443',
'socketio_event': 'add-user',15:['e2k',f'{0x4B} {5}'],'socketio_data_type': 'alert_widget',16:['e2k',f'{0x4F} {5}'],
'amount_tag': 'amount_main','message_tag': 'message','donation_tag': 'donation',25:['e2k',f'{0xC7} {1}']}
with open('profiles/new_profile.pkl', 'wb') as f: pickle.dump(profile, f, pickle.HIGHEST_PROTOCOL)
