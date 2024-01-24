import time
import urllib.request
import json
from PyQt5.QtCore import QObject, pyqtSignal as Signal


class AzureWorker(QObject):
    progress = Signal(str)
    completed = Signal(str)
    error = Signal(str)

    def __init__(self, api_key, account_id, video_url):
        super().__init__()
        self.api_key = api_key
        self.account_id = account_id
        self.video_url = video_url
        self.location = 'trial'
        self.video_name = f'azure-ai-pyqt-{time.time_ns()}'
        self.api_link = 'api.videoindexer.ai'

    def test(self):
        self.log(f"API_KEY: {self.api_key}")
        self.log(f"ACCOUNT_ID: {self.account_id}")
        self.log(f"VIDEO_URL: {self.video_url}")
        time.sleep(10)
        self.exit()

    # Get access token using Account ID
    def getAccessToken(self):
        self.progress.emit("Retrieving Access Token...")
        try:
            url = f"https://{self.api_link}/Auth/{self.location}/Accounts/{self.account_id}/AccessToken?allowEdit=true"

            hdr = {
                'Cache-Control': 'no-cache',
                'Ocp-Apim-Subscription-Key': self.api_key,
            }

            req = urllib.request.Request(url, headers=hdr)
            req.get_method = lambda: 'GET'
            response = urllib.request.urlopen(req)

            self.progress.emit(
                f"[{response.getcode()}] Access Token Retrieved")
            utf_str = response.read().decode('utf-8')
            self.access_token = json.loads(utf_str)
        except Exception as e:
            self.error.emit(f"Access Token Retrieval Failed: {e}")
            raise e

    # Upload video to Azure Video Indexer
    def uploadVideo(self):
        self.progress.emit("Uploading video to Azure...")
        try:
            url = f"https://{self.api_link}/{self.location}/Accounts/{self.account_id}/Videos?name={self.video_name}&videoUrl={self.video_url}&accessToken={self.access_token}"

            hdr = {
                'Cache-Control': 'no-cache',
            }

            req = urllib.request.Request(url, headers=hdr)
            req.get_method = lambda: 'POST'
            response = urllib.request.urlopen(req)

            self.progress.emit(f"[{response.getcode()}] Video uploaded")

            utf_str = response.read().decode('utf-8')
            video_json = json.loads(utf_str)
            print(video_json)
            self.video_id = video_json["id"]
        except Exception as e:
            self.error.emit(f"Video Upload to Azure Video Indexer Failed: {e}")
            raise e

    # Get video index information
    def getVideoIndex(self):
        self.progress.emit("Retrieving video index...")
        try:
            url = f"https://{self.api_link}/{self.location}/Accounts/{self.account_id}/Videos/{self.video_id}/Index?accessToken={self.access_token}"

            hdr = {
                'Cache-Control': 'no-cache',
            }

            index_json = None

            # Check processing progress
            while True:
                req = urllib.request.Request(url, headers=hdr)
                req.get_method = lambda: 'GET'
                response = urllib.request.urlopen(req)

                utf_str = response.read().decode('utf-8')
                index_json = json.loads(utf_str)

                processing_state = index_json['state']
                processing_progress = index_json['videos'][0]['processingProgress']

                if (processing_state not in ['Uploaded', 'Processing']):
                    self.progress.emit(
                        f"[{response.getcode()}] Video index retrieved")
                    break
                else:
                    self.progress.emit(
                        f"[{processing_progress}] {processing_state}...")
                    time.sleep(10)

            with open('index.json', 'w') as fp:
                json.dump(index_json, fp)
            self.progress.emit("Saved to index.json")
        except Exception as e:
            self.error.emit(e)
            raise e

    def exec(self):
        try:
            self.progress.emit(
                "=== Executing Azure Video Indexer Functions ===")
            self.getAccessToken()
            self.uploadVideo()
            self.getVideoIndex()
            self.completed.emit("Completed")
        except Exception:
            return
