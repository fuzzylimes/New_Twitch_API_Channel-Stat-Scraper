import requests, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import creds as CREDS

REG_URL = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(CREDS.CLIENT_ID, CREDS.SECRET)

class User():
    def __init__(self, user_name):
        res = requests.post(REG_URL)
        if res.status_code != 200:
            print("Error grabbing token from server")
        else:
            self.token = res.json()['access_token']
            self.authHeader = {'Authorization': 'Bearer ' + self.token, 'Client-ID': CREDS.CLIENT_ID}
            self.userData = requests.get("https://api.twitch.tv/helix/users?login="+user_name, headers=self.authHeader).json()
            data = self.userData['data'][0]
            self.user_id = data['id']
            self.user_name = data['display_name']
            self.user_image = data['profile_image_url']
            self.user_background = data['offline_image_url']