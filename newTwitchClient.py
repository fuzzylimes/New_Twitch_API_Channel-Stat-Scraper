import creds as CREDS
import requests, json

REG_URL = "https://api.twitch.tv/kraken/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(CREDS.CLIENT_ID, CREDS.SECRET)

class TwitchApi():
    def __init__(self):
        res = requests.post(REG_URL)
        if res.status_code != 200:
            print("Error grabbing token from server")
        else:
            self.token = res.json()['access_token']
            self.authHeader = {'Authorization': 'Bearer ' + self.token}
    
    def GetGames(self, gid=None, name=None):
        if gid==None and name==None:
            return {"response":"Require parameter missing"}
        if gid!=None:
            return requests.get("https://api.twitch.tv/helix/games?id="+gid, headers=self.authHeader)
        else:
            return requests.get("https://api.twitch.tv/helix/games?name="+name, headers=self.authHeader)

    def GetUserId(self, login):
        req = requests.get("https://api.twitch.tv/helix/users?login="+login, headers=self.authHeader)
        if req.status_code != 200:
            return {"response":"User not found!"}
        req = req.json()
        return req['data'][0]['id']

    def GetUserInfo(self, login):
        req = requests.get("https://api.twitch.tv/helix/users?login="+login, headers=self.authHeader)
        if req.status_code != 200:
            return {"response":"User not found!"}
        return req.json()

    def GetChannelInfo(self, uid=None, login=None):
        if uid==None and login==None:
            return {"response":"Require parameter missing"}
        if uid!=None:
            req = requests.get("https://api.twitch.tv/helix/streams?user_id="+uid, headers=self.authHeader)
            if req.status_code != 200:
                return {"response":"User not found!"}
            if len(req.json()['data']) < 1:
                return {"response":"User not online"}
            req = req.json()
            return req
        else:
            req = requests.get("https://api.twitch.tv/helix/streams?user_login="+login, headers=self.authHeader)
            if req.status_code != 200:
                return {"response":"User not found!"}
            if len(req.json()['data']) < 1:
                return {"response":"User not online"}
            req = req.json()
            return req

    def GetChatters(self, cid=None):
        if cid == None:
            return {"response":"Required channelId parameter missing!"}
        req = requests.get("https://tmi.twitch.tv/group/user/{}/chatters".format(cid))
        return {
            "chatter_count": req.json()['chatter_count'],
            "mods": len(req.json()['chatters']['moderators']),
            "staff": len(req.json()['chatters']['staff']),
            "admins": len(req.json()['chatters']['admins']),
            "global_mods": len(req.json()['chatters']['global_mods']),
            "viewers": len(req.json()['chatters']['viewers'])
        }
    
    def GetFollowers(self, id):
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': CREDS.CLIENT_ID
        }
        followers = requests.get('https://api.twitch.tv/kraken/channels/24761645/follows?limit=1', headers=headers).json()['_total']
        return followers