import time
import urllib.request
import json

# CONSTANTS
LOCATION = 'trial'
VIDEO_NAME = f'azure-ai-pyqt-{time.time_ns()}'
API_LINK = "api.videoindexer.ai"

# USER INPUT
ACCOUNT_ID = 'INSERT_ACCOUNT_ID'
API_KEY = 'INSERT_API_KEY'
VIDEO_URL = 'INSERT_VIDEO_URL'

# VARIABLES
ACCESS_TOKEN = None
VIDEO_ID = None
VIDEO_ACCESS_TOKEN = None

########### GET ACCESS TOKEN USING ACCOUNT ID #############
print("Retrieving Access Token...")
try:
    url = f"https://{API_LINK}/Auth/{LOCATION}/Accounts/{ACCOUNT_ID}/AccessToken?allowEdit=true"

    hdr = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': API_KEY,
    }

    req = urllib.request.Request(url, headers=hdr)
    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)

    print(f"[{response.getcode()}] Access Token Retrieved")
    utf_str = response.read().decode('utf-8')
    ACCESS_TOKEN = json.loads(utf_str)
except Exception as e:
    print(e)

########### UPLOAD VIDEO TO AZURE VIDEO INDEXER #############
print("Uploading video to Azure...")
try:
    url = f"https://{API_LINK}/{LOCATION}/Accounts/{ACCOUNT_ID}/Videos?name={VIDEO_NAME}&videoUrl={VIDEO_URL}&accessToken={ACCESS_TOKEN}"

    hdr = {
        'Cache-Control': 'no-cache',
    }

    req = urllib.request.Request(url, headers=hdr)
    req.get_method = lambda: 'POST'
    response = urllib.request.urlopen(req)

    print(f"[{response.getcode()}] Video uploaded")

    utf_str = response.read().decode('utf-8')
    video_json = json.loads(utf_str)
    VIDEO_ID = video_json["id"]
except Exception as e:
    print(e)

########### GET VIDEO INDEX INFORMATION #############
print("Retrieving video index...")
try:
    url = f"https://{API_LINK}/{LOCATION}/Accounts/{ACCOUNT_ID}/Videos/{VIDEO_ID}/Index?accessToken={ACCESS_TOKEN}"

    hdr = {
        'Cache-Control': 'no-cache',
    }

    index_json = None

    while True:
        req = urllib.request.Request(url, headers=hdr)
        req.get_method = lambda: 'GET'
        response = urllib.request.urlopen(req)

        utf_str = response.read().decode('utf-8')
        index_json = json.loads(utf_str)

        processing_state = index_json['state']
        processing_progress = index_json['videos'][0]['processingProgress']

        if (processing_state not in ['Uploaded', 'Processing']):
            print(f"[{response.getcode()}] Video index retrieved")
            break
        else:
            print(f"[{processing_progress}] {processing_state}...")
            time.sleep(10)

    with open('index.json', 'w') as fp:
        json.dump(index_json, fp)
    print("Saved to index.json")

except Exception as e:
    print(e)
