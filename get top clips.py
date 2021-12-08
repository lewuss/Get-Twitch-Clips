import requests
import json

BASE_URL = 'https://api.twitch.tv/helix/'
authURL = 'https://id.twitch.tv/oauth2/token'

keys = open("newkeys.txt", 'r')

CLIENT_ID = keys.readline().strip()
token = keys.readline().strip()

INDENT = 2

AutParams = {'client_id': CLIENT_ID,
             'client_secret': token,
             'grant_type': 'client_credentials'
             }

AUTCALL = requests.post(url=authURL, params=AutParams)
ACCESS_TOKEN = AUTCALL.json()['access_token']
HEADERS = {'Client-ID': CLIENT_ID, 'Authorization': "Bearer " + ACCESS_TOKEN}


def get_clips_by_user_all(id, start_date, end_date):
    clips = []
    pagination = ""
    isNext = True
    start = f'{start_date}T07:20:50.52Z'
    end = f'{end_date}T07:20:50.52Z'
    while isNext:
        url = f"{BASE_URL}clips?broadcaster_id={id}&first=100&after={pagination}&started_at={start}&ended_at={end}"
        response = requests.get(url, headers=HEADERS).json()
        if 'cursor' in response['pagination']:
            pagination = response['pagination']['cursor']
        else:
            isNext = False
        clips.extend(response['data'])
    return clips


def get_clips_by_user_num(id, start_date, end_date, num):
    clips = []
    pagination = ""
    start = f'{start_date}T07:20:50.52Z'
    end = f'{end_date}T07:20:50.52Z'
    for x in range(num // 100):
        url = f"{BASE_URL}clips?broadcaster_id={id}&first=100&after={pagination}&started_at={start}&ended_at={end}"
        response = requests.get(url, headers=HEADERS).json()
        if 'cursor' in response['pagination']:
            pagination = response['pagination']['cursor']
        else:
            break
        clips.extend(response['data'])
    return clips


def get_clips_by_user(id, start_date, end_date):
    clips = []
    start = f'{start_date}T07:20:50.52Z'
    end = f'{end_date}T07:20:50.52Z'
    url = f"{BASE_URL}clips?broadcaster_id={id}&first=20&started_at={start}&ended_at={end}"
    response = requests.get(url, headers=HEADERS).json()
    clips.extend(response['data'])
    return clips


def get_user_id(user_login):
    query = f'{BASE_URL}users?login={user_login}'
    response = requests.get(query, headers=HEADERS)
    return response.json()['data'][0]['id']


data = []
filename = input("Enter File with Usernames ")
start_date = input("Enter Start Date (Format YYYY-MM-DD) ")
end_date = input("Enter End Date (Format YYYY-MM-DD) ")
number_of_clips = input("Enter number of clips (multiplicity of 100). If want to get all type ALL ")
if number_of_clips.lower() == "all":
    all = True
else:
    all = False
    number_of_clips = int(number_of_clips)
with open(filename, 'r', encoding='UTF-8') as file:
    users = file.readlines()
    for user in users:
        id = get_user_id(user.strip())
        if all:
            clips = get_clips_by_user_all(id, start_date, end_date)
        else:
            clips = get_clips_by_user_num(id, start_date, end_date, number_of_clips)
        tmp_data = {'name': user.strip(),
                    'clips': clips}
        print(tmp_data)
        data.append(tmp_data)
        print(user.strip(), "done.")

with open('data.json', 'w', encoding='UTF-8') as f:
    json.dump(data, f)
