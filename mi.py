import requests
from requests.auth import _basic_auth_str
import json
import os.path
import sys
import json



client_secret = "ccb627a583d45e1e70e5c1cf6aa7925e"
client_id = "mailchimp"
grant_type = "password"
username = "100@b1communications"
password = "^MD@l6vL&3ZL!omC"


url = "https://core1.b1communications.ca/ns-api/oauth2/token/"
domain = ""
access_token   = ""
refresh_token = ""


payload = {
    "client_secret": client_secret,
    "client_id": client_id,
    "grant_type": grant_type,
    "username": username,
    "password": password
}

headers = {
    "Content-Type": "application/json"
}


response = requests.get(url, data=json.dumps(payload), headers=headers)



if response.status_code == 200:
    data = response.json()
    
    access_token = data['access_token']

    refresh_token = data['refresh_token']
    domain = data['domain']
    
else:
    print("Error:", response.status_code)


api_headers = {
  
        "Authorization": f"Bearer {access_token}"
        }


payload_user = {"domain": "b1communications","srv_code":""}
list_user = []

user_url = "https://core1.b1communications.ca/ns-api/?format=json&object=subscriber&action=read"
response_user = requests.post(user_url, data = payload_user, headers=api_headers)

if response_user.status_code == 200:
    data = response_user.json()
    

    df = pd.DataFrame(data)
    df = df[~df['srv_code'].str.contains('system')]
    df = df[~df['email'].str.contains('u@u.com')]
    df = df[~df['last_name'].str.contains('delete')]
    df = df[~df['last_name'].str.contains('DELETE')]

else:
    print("Error:", response_user.status_code)

#585bfe9432fa835b2e2e37f906011025-us17
list_user = df['user'].tolist()

model = {}
for user in list_user:
    payload_user = {"domain": "b1communications","srv_code":user}

    user_url = "https://core1.b1communications.ca/ns-api/?format=json&object=device&action=read"
    response_user = requests.post(user_url, data = payload_user, headers=api_headers)
    if response_user.status_code == 200:
        data = response_user.json()
        
        for value in data:
            #print(value)
            if user == value['subscriber_name']:
                if 'model' in value:
                    #print(value['model'],user) 
                    model[user] = value['model']
                    df.loc[df['user'] == user, 'model'] = value['model']



df['model'] = df['model'].fillna('')


from mailchimp_marketing import Client

mailchimp = Client()
mailchimp.set_config({
  "api_key": "585bfe9432fa835b2e2e37f906011025-us17",
  "server": "us17"
})

response = mailchimp.ping.get()
list_id = ""
interest_category = ""
interest = ""

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import mailchimp_marketing as MailchimpMarketing





try:
  client = MailchimpMarketing.Client()
  client.set_config({
    "api_key": "585bfe9432fa835b2e2e37f906011025-us17",
    "server": "us17"
  })

  response = client.lists.get_all_lists()
  list_id = response["lists"][0]['id']


except ApiClientError as error:
  print("Error: {}".format(error.text))

#get interest category id from mail chimp############################


import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

try:
  client = MailchimpMarketing.Client()
  client.set_config({
    "api_key": "585bfe9432fa835b2e2e37f906011025-us17",
    "server": "us17"
  })
  response = client.lists.get_list_interest_categories(list_id)
  
  for data in response['categories']:
    if data['title'] == 'Customer':       
        interest_category = data['id']

except ApiClientError as error:
  print("Error: {}".format(error.text))


#get interest category id from mail chimp############################



#get interest  id from mail chimp from interest category id and list id############################



import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

try:
  client = MailchimpMarketing.Client()
  client.set_config({
    "api_key": "585bfe9432fa835b2e2e37f906011025-us17",
    "server": "us17"
  })

  response = client.lists.list_interest_category_interests(list_id, interest_category)

  interest = response['interests'][0]['id']

  
except ApiClientError as error:
  print("Error: {}".format(error.text))



data_netsapians = df['email'].tolist()
data_mailchimp = []
update_members = []
add_members = []
delete_members  = []
add_members_member_info = []
update_members_member_info = []
delete_members_member_info = []

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

try:
  client = MailchimpMarketing.Client()
  client.set_config({
  "api_key": "585bfe9432fa835b2e2e37f906011025-us17",
  "server": "us17"
  })

  response = client.lists.get_list_members_info(list_id)
  for data in response ['members']:

    
    if data['email_address'] in data_netsapians:
        update_members.append(data['email_address'])


    if data['email_address'] not in data_netsapians:
        delete_members.append(data['email_address'])



  

except ApiClientError as error:
  print("Error: {}".format(error.text))




add_members = data_netsapians


add_members = [x for x in add_members if x not in delete_members]

add_members = [x for x in add_members if x not in update_members]


for data in update_members:
    matching_rows = df.loc[df['email'] == data]

    if not matching_rows.empty:
        member_info = {
            "email_address": matching_rows['email'].iloc[0],
            "status": "subscribed",
            "merge_fields": {
                "FNAME": matching_rows['first_name'].iloc[0],
                "LNAME": matching_rows['last_name'].iloc[0],
                'COMPANY': matching_rows['domain'].iloc[0],
                "EXT": matching_rows['user'].iloc[0],
                'PHONE': matching_rows['callid_nmbr'].iloc[0],
                'USERNAME': matching_rows['subscriber_login'].iloc[0],
                'SCOPE': matching_rows['scope'].iloc[0],
                'DEVICE': matching_rows['model'].iloc[0],
                "ADDRESS": {
                    "addr1": "123",
                    "city": "Toronto",
                    "state": "Canada",
                    "zip": matching_rows['area_code'].iloc[0]
                }
            },
            "interests": {
                interest: True
            }
        }
        update_members_member_info.append(member_info)
    else:
        print("No matching rows found for email:", data)          


print(add_members)


for data in add_members:
    matching_rows = df.loc[df['email'] == data]

    if not matching_rows.empty:
        member_info = {
            "email_address": matching_rows['email'].iloc[0],
            "status": "subscribed",
            "merge_fields": {
                "FNAME": matching_rows['first_name'].iloc[0],
                "LNAME": matching_rows['last_name'].iloc[0],
                'COMPANY': matching_rows['domain'].iloc[0],
                "EXT": matching_rows['user'].iloc[0],
                'PHONE': matching_rows['callid_nmbr'].iloc[0],
                'USERNAME': matching_rows['subscriber_login'].iloc[0],
                'SCOPE': matching_rows['scope'].iloc[0],
                'DEVICE': matching_rows['model'].iloc[0],
                "ADDRESS": {
                    "addr1": "123",
                    "city": "Toronto",
                    "state": "Canada",
                    "zip": matching_rows['area_code'].iloc[0]
                }
            },
            "interests": {
                interest: True
            }
        }
        add_members_member_info.append(member_info)
        
    else:
        print("No matching rows found for email:", data)          





for data in delete_members:
    matching_rows = df.loc[df['email'] == data]

    if not matching_rows.empty:
        member_info = {
            "email_address": matching_rows['email'].iloc[0],
            "status": "subscribed",
            "merge_fields": {
                "FNAME": matching_rows['first_name'].iloc[0],
                "LNAME": matching_rows['last_name'].iloc[0],
                'COMPANY': matching_rows['domain'].iloc[0],
                "EXT": matching_rows['user'].iloc[0],
                'PHONE': matching_rows['callid_nmbr'].iloc[0],
                'USERNAME': matching_rows['subscriber_login'].iloc[0],
                'SCOPE': matching_rows['scope'].iloc[0],
                'DEVICE': matching_rows['model'].iloc[0],
                "ADDRESS": {
                    "addr1": "123",
                    "city": "Toronto",
                    "state": "Canada",
                    "zip": matching_rows['area_code'].iloc[0]
                }
            },
            "interests": {
                interest: True
            }
        }
        delete_members_member_info.append(member_info)
    else:
        print("No matching rows found for email:", data)          



#update members ################

try:
    client = MailchimpMarketing.Client()
    client.set_config({
    "api_key": "585bfe9432fa835b2e2e37f906011025-us17",
    "server": "us17"
    })
    for row in update_members_member_info:
        try:
            
            if row['merge_fields']['SCOPE'] == 'Super User':
                row['merge_fields']['SCOPE'] = 'Office Manager'

            response = client.lists.update_list_member(list_id,row['email_address'],row)
        except ApiClientError as error:
            print("Error: {}".format(error.text))

except ApiClientError as error:
    print("Error: {}".format(error.text))



#update members ################

#################ADD MEMBERS ########################################



try:
    client = MailchimpMarketing.Client()
    client.set_config({
    "api_key": "585bfe9432fa835b2e2e37f906011025-us17",
    "server": "us17"
    })
    for row in add_members_member_info:
        print(row)
        try:
            if row and 'merge_fields' in row:
                if row['merge_fields']['SCOPE'] == 'Super User':
                    row['merge_fields']['SCOPE'] = 'Office Manager'
            response = client.lists.add_list_member(list_id, row)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
except ApiClientError as error:
    print("Error: {}".format(error.text))








#################ADD MEMBERS ########################################
print("firqa",delete_members_member_info)
try:
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": "585bfe9432fa835b2e2e37f906011025-us17",
        "server": "us17"
    })
    if len(delete_members_member_info) > 0 :
        for row in delete_members_member_info:
            try:
                if row['merge_fields']['SCOPE'] == 'Super User':
                    row['merge_fields']['SCOPE'] = 'Office Manager'
                response = client.lists.delete_list_member(list_id, row['email_address'])
            except ApiClientError as error:
                print("Error: {}".format(error.text))
except ApiClientError as error:
    print("Error: {}".format(error.text))

