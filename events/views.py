import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pymongo
import json
import os


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


# Create your views here.
photo_url = ""
client = pymongo.MongoClient('mongodb+srv://jordantab:Tarkan12@cluster0.02rmati.mongodb.net/?retryWrites=true&w=majority')

def Home(request):
    response = 'hey'
    return HttpResponse(response)

@csrf_exempt
def verifyLogin(request):
    # process user input

    data = request.read().decode("utf-8")

    # convert the json string to a dictionary
    data = json.loads(data)

    # extract the value of the "username" key
    username_input = data.get("username")

    # extract the value of the "password" key
    password_input = int(data.get("password"))

    # get user with matching username
    foramd_db = client['forAMD']
    collection = foramd_db['Users']

    response = False
    user = collection.find({"username":username_input})

    for temp in user:
        # print(temp)
        if password_input == temp['password']:
            response = True

    return HttpResponse(response)



@csrf_exempt
def getAlbum(request):
    
    input = request.read().decode("utf-8")
    # convert the json string to a dictionary
    input = json.loads(input)

    # extract the value of the "username" key
    album_name = input.get("label")

    ids = {
        'Newport': 'APtRtIHbM5GXXGxHhD3WbESJpfkxJw8NA1qIZRrfwuPJndB5iq6_L6_ROlNozjxgd1HXXYreeJvV',
        'Nextdoor': 'APtRtIERvTsFSuipo5o5mLTCdP3nzZcY_QcEWZFQx39oS9H_aBjtFdbvlg0b3h_Fh8PASfHOLXKM',
        'Icon': 'APtRtIGXG-5Rd6vlMp05P3mK-mp9zAsc6iQ2Gpm9OSA2dhdBNWLvyO830UyYWsmE6Pdkz5-QIFME',
        'Brookline Park': 'APtRtIH3lz1TDaairLallmrt1rRvj1TJ71jRy_dStZtO1c6c0_Wn1oS4SavkWyAc2NHggbtuZIHK',
        'TITS': 'APtRtIGODqH3FxlIerKlkkLNp7p7bvEfN3Q91GZYQVOy9TmWXT3supOtEbryPnMTFBLcQ2Fxc-ex',
        'Red Sox Game': 'APtRtIH7cf6SnHQgIA6U-UTVig7EOqbAaJ4GTrsjhWRbFAGQbW5UfbmdpBJG7NKhCWZ8G509VBsP',
        'Bay State Bench': 'APtRtIFII3bcI2dtgPqXU4NhW_M8R-39wEDFAd2T-OQBgIokfiAVjmW_o68nTedkb-8UlzoJ4f22',
        'Manti, Wine, Face Masks': 'APtRtIEWYZ4Ro935Czt0Ycglt3SBGtvEsR59gGrJVyrq-2S28KD35hc2TcGte1SsRyPBGZySu8_V',
        'Korean BBQ': 'APtRtIEv0BQ2uLHI3NmXZe53wfrzZGbbkiQj8N0lDrunBYp7WfvFEnoTqnKZv9Xs0CIqbyUjjjql',
        'Celtics Game': 'APtRtIFQ_ZTV7MBybqUaapaV0pz6WleGW-GOugCB1NeiYDNLnxtknhlXXSQVR8Tiqr-fLNHTV6LC',
        'Halloween': 'APtRtIFECpKyFy7kLmLdPzGZG1rfVoadJHs0tKn4PoFJssmbRC6zmohutO8cN6MXQdstUkXvoyh-',
        'Lola42': 'APtRtIGqw5l8TYVoMJaSydv16L1VlTDrQB9KHAcd4bJvlGNIAYPvnGGaKlLOI8KWPXbOdzN-8mPi',
        'Italian Cooking Class': 'APtRtIH59cNxIyIavueIWLV3wYxo1LuPlm0NRiim2GlCZ4CeMtPK3iKbD0K_qcKXX8yy4L9u-o_-',
        'Athlete Formal': 'APtRtIHzy25gKdZzrBovLzumo9qPNihalJbypYCB_7N1IZZs-hdUq5lrjn7Jl-jnMeeJ0TWJpkv3',
        'JT 22nd Birthday': 'APtRtIGTzm_wnTmUnAmoN2shtyUyaApmuDWtF2ZSuhtVsbDeys5sj3g37MdseuiGnhJThd9iPGc3',
        'Christmas': 'APtRtIEthKwNq_IJ7QX-ew2AsNvRSuyLbm3OUGEGNWUBKOeP44jlBQgYULMQ9kdN7LtQbUZVavNW',
        'NYE': 'APtRtIFzZT4EYhdR6WMWLsmllaUet-MoAm5tiZ6lUHwLg3acyMCW-KbticVvQ_pMiwiFotZcaTzS'
        }
        
    album_id = ids[album_name]
    # print(album_id)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/tarkantaboglu/Desktop/Random Projects/forAMD/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
        
        # specify the album id of the requested album 
        request_body = {
            'albumId': album_id,
            'pageSize': 25
        }

        # get the first 25 files in the album
        response = service.mediaItems().search(body = request_body).execute()
        lst_medias = response.get('mediaItems')
        nextPageToken = response.get('nextPageToken')

        # get the rest of the files
        while nextPageToken:
            request_body['pageToken'] = nextPageToken

            response = service.mediaItems().search(body = request_body).execute()
            lst_medias.extend(response.get('mediaItems'))
            nextPageToken = response.get('nextPageToken')

        df_files = pd.DataFrame(lst_medias)
        
        #extract the mediaItemIds of the files
        mediaItemIds = df_files['id'].tolist()

        photos = service.mediaItems().batchGet(mediaItemIds=mediaItemIds).execute()
        photos = photos.get('mediaItemResults')
        df_photos = pd.DataFrame(photos)
        df_photos = df_photos['mediaItem'].apply(pd.Series)
        base_urls = df_photos['baseUrl'].tolist()
        response = HttpResponse(json.dumps(base_urls))
        # response = service.albums().get(albumId = album_id).execute()
        # cover_photo_id = response['coverPhotoMediaItemId']
        # photo = service.mediaItems().batchGet(mediaItemIds=[cover_photo_id]).execute()
        # print(photo)
        # photo_url = photo['baseUrl']
        # response = HttpResponse(photo_url)
        # response["Access-Control-Allow-Origin"] = "*"
        # response["Access-Control-Allow-Methods"] = "POST"
        # response["Access-Control-Allow-Headers"] = "Content-Type"
        # response["Access-Control-Allow-Credentials"] = "true"
        # response["Cross-Origin-Resource-Policy"] = "cross-origin"
        
    except HttpError as err:
        print(err)

    return response

@csrf_exempt
def verifyPuzzle(request):
     # process user input

    data = request.read().decode("utf-8")

    # convert the json string to a dictionary
    data = json.loads(data)

    # extract the puzzle number
    puzzle_input = data.get("puzzle")

    # extract the value of the "answer" key
    answer_input = data.get("answer")

    # get solution
    foramd_db = client['forAMD']
    collection = foramd_db['Puzzles']
    
    response = False
    solution = collection.find({"puzzle_number":puzzle_input})

    for temp in solution:
        if answer_input == temp['answer']:
            response = True

    return HttpResponse(response)

@csrf_exempt
def temp(request):
    print(1)
    foramd_db = client['forAMD']
    collection = foramd_db['Nextdoor']
    solution = collection.find({},{"_id":0})
    for temp in solution:
        solution = temp['url']
    return HttpResponse(solution)