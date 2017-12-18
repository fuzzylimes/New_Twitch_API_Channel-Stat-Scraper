import requests, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import creds as CREDS

REG_URL = "https://api.twitch.tv/kraken/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(CREDS.CLIENT_ID, CREDS.SECRET)

class html():
    def __init__(self, user_name):
        res = requests.post(REG_URL)
        if res.status_code != 200:
            print("Error grabbing token from server")
        else:
            self.token = res.json()['access_token']
            self.authHeader = {'Authorization': 'Bearer ' + self.token}
            self.userData = requests.get("https://api.twitch.tv/helix/users?login="+user_name, headers=self.authHeader).json()
            data = self.userData['data'][0]
            self.user_name = data['display_name']
            self.user_image = data['profile_image_url']
            self.user_background = data['offline_image_url']

    def header(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Sample Page</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
    <script defer src="https://use.fontawesome.com/releases/v5.0.1/js/all.js"></script>
    <link rel="stylesheet" href="style.css">

</head>
<body id="bootstrap-overrides">
    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #6441a5">
        <a class="navbar-brand" href="#">FuzzyStats</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup"
            aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Streamers
                    </a>
                    <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                        <a class="dropdown-item" href="#">TimTheTatman</a>
                        <a class="dropdown-item" href="#">Lirik</a>
                        <a class="dropdown-item" href="#">Cirno_tv</a>
                    </div>
                </li>
            </div>
        </div>
    </nav>"""

    def streamer(self):
        return """<div class="container mt-4">
        <div class="row">
            <div class="col text-center mb-1">
                <p id="stream_name">{0}</p>
                <p id="stream_link"><a href="http://www.twitch.tv/{0}"><i class="fab fa-twitch"></i> {0}</a></p>
            </div>
        </div>
        <div class="row">
            <div class="col text-center">
                <img src="{1}" alt="">
            </div>
        </div>
    </div>

    """.format(self.user_name, self.user_image)

    def body_one(self, date_index, uptime, game_list):
        a = """            

    <div class="container daily-record">
        <div class="card">
            <div class="card-header" id="heading_{0}" data-toggle="collapse" href="#collapse_{0}" aria-expanded="false" aria-controls="collapse_{0}">
                <h5 class="mb-0">""".format(date_index.replace(':','-'))

        b = """                 <div class="mb-3" id="card_box_title">{0} - {1}</div>
                    <div class="container" id="card_box_display">""".format(date_index.replace(':','-')[:10], uptime)
        
        c = ""
        for item in game_list:
            c = c+"<img src=\"{}\">\n".format(item)

        d = """            </div>
                </h5>
            </div>
            <div id="collapse_{0}" class="collapse" aria-labelledby="heading_{0}">""".format(date_index.replace(':','-'))
        return a+b+c+d

    def body_two(self, game_icon, title, time_played, start_time, end_time, max_viewers, max_chatters):
        return """                <div class="container" id="game_record">
                    <div class="card">
                        <div class="row">
                            <div class="col-md-3 text-center game-box align-self-center">
                                <img src="{}">
                            </div>
                            <div class="col-md-9 align-self-center">
                                <div class="card-block">
                                    <div class="card-title">{} - {}</div>
                                    <div class="card-text">
                                        <table class="table table-striped table-sm">
                                            <tbody>
                                                <tr>
                                                    <td scope="row">Time Played</td>
                                                    <td>{}</td>
                                                </tr>
                                                <tr>
                                                    <td scope="row">Start Time</td>
                                                    <td>{}</td>
                                                </tr>
                                                <tr>
                                                    <td scope="row">End Time</td>
                                                    <td>{}</td>
                                                </tr>
                                                <tr>
                                                    <td scope="row">Max Viewers</td>
                                                    <td>{}</td>
                                                </tr>
                                                <tr>
                                                    <td scope="row">Max Chatters</td>
                                                    <td>{}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>""".format(game_icon, title, time_played, time_played, start_time, end_time, max_viewers, max_chatters)
    def body_three(self):
        return """                </div>
                    </div>
                </div>"""

    def footer(self):
        return """            </div>
        </div>
    </div>

    <!-- Footer -->
    <div class="footer">
        <div class="container">
            <div class="row justify-content-md-center text-center">
                <div class="col-md-auto">
                    <p><a href="https://github.com/fuzzylimes/New_Twitch_API_Channel-Stat-Scraper">
                    <i class="fab fa-7x fa-github" aria-hidden="true"></i></a></p>
                    <p>Made with love by fuzzylimes.</p>
                </div>
            </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>
</body>
</html>"""

