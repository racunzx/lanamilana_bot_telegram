
import json
import requests
from time import sleep
from config import TOKEN
from datetime import datetime
from database.function import DataBaseFunc

url = "https://api.telegram.org/bot" + TOKEN + "/"

def create_requets(methodType,methond, **data):
    if data != None:
        r = requests.request(methodType, url + methond, **data)
    else:
        r = requests.request(methodType, url + methond)
    return r.text

def update_info_user(user):
    actualy_subs = [ph for ph in user.purchased_subscriptions if ph.data_end > datetime.now()]
    
    if (len(actualy_subs) == 0):
        user.is_have_subscription = False
        DataBaseFunc.commit()
    


def kick_user_from_channel(user, channel):
    is_member = json.loads(create_requets("POST", "getChatMember", data = {'chat_id' : channel.id, 'user_id' : user.id}))['ok']
    
    if(is_member):
        response = create_requets("POST", "kickChatMember", data = {'chat_id' : channel.id, 'user_id' : user.id})
    
    update_info_user(user)



all_users = DataBaseFunc.get_users_with_subscribe()
users = [user for user in all_users if user.is_have_subscription]
for user in users:
    for ph in user.purchased_subscriptions:
        for channel in ph.courses.channels:
            try:
                if ph.data_end < datetime.now():
                    kick_user_from_channel(user, channel.channels) 
            except:
                continue
