from urllib import parse

TOKEN = 'MTA0MDk0MTkxMDY0ODQzNDY5MA.GBDeGZ.dOTQtqr17lbvwgxtSkZ82FkEhjwkCAHhr5QiXA'
CLIENT_SECRET = 'Ah86b-O6LJ95_G-_sHeNgGNzOI8gaK4g'
REDIRECT_URI = 'http://ec2-44-211-133-5.compute-1.amazonaws.com/oauth/callback'
OAUTH_URL = f'https://discord.com/api/oauth2/authorize?client_id=1040941910648434690&redirect_uri={parse.quote(REDIRECT_URI)}&response_type=code&scope=identify%20email'
