from urllib import parse
//tokens removed on github
TOKEN = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://ec2-44-211-133-5.compute-1.amazonaws.com/oauth/callback'
OAUTH_URL = f'https://discord.com/api/oauth2/authorize?client_id=1040941910648434690&redirect_uri={parse.quote(REDIRECT_URI)}&response_type=code&scope=identify%20email'
