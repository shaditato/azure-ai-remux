ACCOUNT_ID = 'INSERT_ACCOUNT_ID'
API_KEY = 'INSERT_API_KEY'

########### GET ACCESS KEY USING ACCOUNT ID #############
import urllib.request, json

try:
    url = f"https://api.videoindexer.ai/Auth/trial/Accounts/{ACCOUNT_ID}/AccessToken?allowEdit=false"

    # Request headers
    hdr = {
    'Cache-Control': 'no-cache',
    'Ocp-Apim-Subscription-Key': API_KEY,
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    res_string = response.read().decode('utf-8')
    print(json.loads(res_string))
except Exception as e:
    print(e)
####################################

