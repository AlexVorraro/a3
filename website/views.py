import datetime
import boto3
from boto3.dynamodb.conditions import Attr, Key
from flask import Blueprint, render_template,request,flash, redirect
from website import auth
TABLE_NAME = "Music"
region = 'us-east-1'
bucketName='inteams'
s3 = boto3.resource('s3', aws_access_key_id='ASIAY24XPWCJJD6FII52',
                          aws_secret_access_key='o2x8LGPQsDvZkKM/Kza0DZJ25D+6npZZv3QYp4Ct',
                          aws_session_token='FwoGZXIvYXdzEHUaDLfJxYh5g/+SeCLDjiLNAUIqz59qrBS9gbXkSUeIbElD3utkMitH1brRp3zXyyFXgnFS/bV35NQa3tyuY/J11eg9fmtl3j4+tgm1ysR/eBrKOClNhFuZRjSo2fk9XHeKBMJDjZNo/i59J88i/hvlYfuqZ/6jP4HU15G/FtbW4YHg0qrZwL4S6Mr11mqQK0GgX93qV4wlvxHqVTdwsHguF2uSXVLE4VXf1dwdj9rARAU3YZiQBxrFnc9raALDbUyAzKXO7BCic0cCC4zoNpJwf4wn3on319CfjDYO668o3rrmmwYyLVkmX8LxUkpUwA05oAlOFwN8BVeOfhGRrwAqeOi6o2pUXWuwonhy8UyCZpNLtQ==',
                          region_name=region)
s3=boto3.client('s3')
# s3.Bucket(bucketName).dowload_file('Arcane Fire','suca.jpg')
# file='Arcade Fire'
# cur_path = os.getcwd()
# filename="website/files"
# bucket = s3.Bucket(bucketName)
#----------------------------------------------------------aggiungi credenziali che non funonzia in ec2
dynamodb = boto3.resource('dynamodb', aws_access_key_id='ASIAY24XPWCJJD6FII52',
                          aws_secret_access_key='o2x8LGPQsDvZkKM/Kza0DZJ25D+6npZZv3QYp4Ct',
                          aws_session_token='FwoGZXIvYXdzEHUaDLfJxYh5g/+SeCLDjiLNAUIqz59qrBS9gbXkSUeIbElD3utkMitH1brRp3zXyyFXgnFS/bV35NQa3tyuY/J11eg9fmtl3j4+tgm1ysR/eBrKOClNhFuZRjSo2fk9XHeKBMJDjZNo/i59J88i/hvlYfuqZ/6jP4HU15G/FtbW4YHg0qrZwL4S6Mr11mqQK0GgX93qV4wlvxHqVTdwsHguF2uSXVLE4VXf1dwdj9rARAU3YZiQBxrFnc9raALDbUyAzKXO7BCic0cCC4zoNpJwf4wn3on319CfjDYO668o3rrmmwYyLVkmX8LxUkpUwA05oAlOFwN8BVeOfhGRrwAqeOi6o2pUXWuwonhy8UyCZpNLtQ==',
                          region_name=region)
table = dynamodb.Table(TABLE_NAME)
views = Blueprint('views', __name__)
# s3.download_file(
#                         Bucket=bucketName,
#                         Key=file,
#                         Filename=filename)
# s3.get_obj(bucketName,'Arcade Fire')


@views.route('/home', methods=['GET', 'POST'])
def home():
    print("ooo")
    author = auth.passing()
    passedEmail = auth.passingEmail()
    subscriptions=[]
    img = 's3://musics3907260/Arcade Fire'
    try:
        print("nomhanz")
        table = dynamodb.Table("Users")
        response = table.query(
            KeyConditionExpression=Key('Email').eq(passedEmail)
        )

        sub = ''
        risp=''
        try:
            subs = response["Items"][0]['subs']
            print("1rippe")
            sub = subs.split("-")
            titles = []
            artists = []
            years = []
            for s in sub:
                if s:
                    print(s+" is s")
                    table = dynamodb.Table("Music")
                    print("checkc")
                    risp = table.scan(
                        FilterExpression=Attr('title').eq(s)
                    )
                    # titles.append(s+"-"+risp["Items"][0]['artist']+"-"+risp["Items"][0]['year'])
                    titles.append(s)
                    artists.append(risp["Items"][0]['artist'])
                    years.append(risp["Items"][0]['year'])
            subscriptions = []
            i = 0
            for title in titles:
                subscriptions.append(titles[i] + "-" + artists[i] + "-" + str(years[i]))
                i=i+1
            print(titles)
            print(artists)
            print(years)
            print(subscriptions)
        except Exception as e:
            print(e)
    except:
        print("mhanz")
        # s3.download_file(bucketName,'Arcade Fire','Arcade Fire')



    if request.method == 'POST':

        subpassed=request.form.get('sub')
        if subpassed is not None:
            songpassed=subpassed.split("-")
            # titles.index(songpassed[0])
            print("titoliiii")
            print(titles)
            n=(titles.index(songpassed[0]))
            titles.pop(n)
            print(titles)
            artists.pop(n)
            years.pop(n)

            subs=''
            subscriptions = []
            i=0
            for title in titles:
                subs=subs+titles[i]+"-"
                subscriptions.append(titles[i] + "-" + artists[i] + "-" + str(years[i]))
                i=i+1
            table = dynamodb.Table("Users")
            table.update_item(
                Key={
                    'Email': passedEmail
                },
                UpdateExpression='SET subs =:a',
                ExpressionAttributeValues={
                    ":a": subs
                },
                ReturnValues="UPDATED_NEW"
            )

        song=request.form.get('song')
        print(song)
        subs=''
        if song is not None:
            table = dynamodb.Table("Users")

            response = table.query(
                KeyConditionExpression=Key('Email').eq(passedEmail)
            )
            try:
                subs=response["Items"][0]['subs']
                print(subs)

            except:
                print()

            subs = subs + song
            table.update_item(
                Key={
                    'Email':passedEmail
                },
                UpdateExpression='SET subs =:a',
                ExpressionAttributeValues={
                    ":a":subs+'-'
                },
                ReturnValues="UPDATED_NEW"
            )

            table = dynamodb.Table("Users")
            response = table.query(
                KeyConditionExpression=Key('Email').eq(passedEmail)
            )

            sub = ''
            risp = ''
            try:
                subs = response["Items"][0]['subs']
                print("1rippe")
                sub = subs.split("-")
                titles = []
                artists = []
                years = []
                for s in sub:
                    if s:
                        print(s + " is s")
                        table = dynamodb.Table("Music")
                        print("checkc")
                        risp = table.scan(
                            FilterExpression=Attr('title').eq(s)
                        )
                        # titles.append(s+"-"+risp["Items"][0]['artist']+"-"+risp["Items"][0]['year'])
                        titles.append(s)
                        artists.append(risp["Items"][0]['artist'])
                        years.append(risp["Items"][0]['year'])
                subscriptions = []
                i = 0
                for title in titles:
                    subscriptions.append(titles[i] + "-" + artists[i] + "-" + str(years[i]))
                    i = i + 1
                print(titles)
                print(artists)
                print(years)
                print(subscriptions)
            except Exception as e:
                print(e)
            return render_template("home.html", user=author, subscriptions=subscriptions)
        else:
            table = dynamodb.Table("Music")
            title=request.form.get('title')
            artist = request.form.get('artist')
            try:
                year = int(request.form.get('year'))
            except:
                year=request.form.get('year')
            response=''

            if title:
                if artist:
                    if year:
                        response = table.scan(
                            FilterExpression=Attr('title').eq(title) & Attr('artist').eq(artist) & Attr('year').eq(year)
                        )
                    else:
                        response = table.scan(
                            FilterExpression=Attr('title').eq(title) & Attr('artist').eq(artist)
                        )
                elif year:
                    response = table.scan(
                        FilterExpression=Attr('title').eq(title) & Attr('year').eq(year)
                    )
                else:
                    response = table.scan(
                        FilterExpression=Attr('title').eq(title)
                    )
            elif artist:
                if year:
                    response = table.scan(
                        FilterExpression=Attr('artist').eq(artist) & Attr('year').eq(year)
                    )
                else:
                    response = table.scan(
                        FilterExpression=Attr('artist').eq(artist)
                    )
            elif year:
                response = table.scan(
                    FilterExpression=Attr('year').eq(year)
                )

            try:
                response["Items"][0]['year']
                print(response)
                return render_template("home.html",user=author,songs=response["Items"],subscriptions=subscriptions)
            except:
                if subpassed is not None:
                    print()
                else:
                    flash("No result is retrieved. Please query again", category='error')




    return render_template("home.html",user=author,subscriptions=subscriptions,image=img)

@views.route('/fortnite', methods=['GET','POST'])
def fornite():
    url = s3.generate_presigned_url('get_object',
                              Params={
                                  'Bucket':bucketName,
                                  'Key': 'fortnite.jpg'

                              },
                              ExpiresIn=3600)
    table = dynamodb.Table("Videogames")
    description = table.scan(FilterExpression=Attr("title").eq('Fortnite'))['Items']
    desc=''
    for d in description:
        desc = d['description']

    author = auth.passing()
    messages=[]
    authors=[]
    timestamps=[]
    information=[]
    table = dynamodb.Table("Messages")
    data=table.scan(FilterExpression=Attr("videogame").eq('Fortnite'))
    response = data['Items']
    try:
        for mess in response:
            messages.append(mess['message'])
            authors.append(mess['username'])
            timestamps.append(mess['timestamp'])
        i=0
        for a in authors:
            information.append("("+timestamps[i]+") | "+authors[i]+': '+messages[i])
            i=i+1

    except:
        print("")


    if request.method == 'POST' and author!='':
        post = request.form.get('message')
        table = dynamodb.Table('Messages')
        table.put_item(
            Item={
                'username' : author,
                'timestamp' : str(datetime.datetime.now()),
                'videogame' : 'Fortnite',
                'message' : post,
        })
        return redirect('/fortnite')

    return render_template("fortnite.html",messages=information,user=author,desc=desc,url=url)

@views.route('/rocketLeague', methods=['GET','POST'])
def rocketLeague():
    url = s3.generate_presigned_url('get_object',
                                    Params={
                                        'Bucket': bucketName,
                                        'Key': 'rocketLeague.jpg'

                                    },
                                    ExpiresIn=3600)
    table = dynamodb.Table("Videogames")
    description = table.scan(FilterExpression=Attr("title").eq('Rocket League'))['Items']
    desc=''
    for d in description:
        desc = d['description']

    author = auth.passing()
    messages = []
    table = dynamodb.Table("Messages")
    data = table.scan(FilterExpression=Attr("videogame").eq('Rocket League'))
    response = data['Items']
    try:
        for mess in response:
            messages.append(mess['message'])

    except:
        print("")

    if request.method == 'POST' and author!='':
        post = request.form.get('message')
        table = dynamodb.Table('Messages')
        table.put_item(
            Item={
                'username' : author,
                'timestamp' : str(datetime.datetime.now()),
                'videogame' : 'Rocket League',
                'message' : post,
        })
        return redirect('/rocketLeague')

    return render_template("rocketLeague.html",messages=messages,user=author,desc=desc,url=url)

@views.route('/seaOfThieves', methods=['GET','POST'])
def seaOfThieves():
    url = s3.generate_presigned_url('get_object',
                                    Params={
                                        'Bucket': bucketName,
                                        'Key': 'sea OfThieves.jpg'

                                    },
                                    ExpiresIn=3600)
    table = dynamodb.Table("Videogames")
    description = table.scan(FilterExpression=Attr("title").eq('Sea of Thieves'))['Items']
    print(description)
    desc=''
    for d in description:
        desc = d['description']

    author = auth.passing()

    messages = []
    table = dynamodb.Table("Messages")
    data = table.scan(FilterExpression=Attr("videogame").eq('Sea Of Thieves'))
    response = data['Items']
    try:
        for mess in response:
            messages.append(mess['message'])

    except:
        print("")

    if request.method == 'POST' and author != '':
        post = request.form.get('message')
        table = dynamodb.Table('Messages')
        table.put_item(
            Item={
                'username': author,
                'timestamp': str(datetime.datetime.now()),
                'videogame': 'Sea Of Thieves',
                'message': post,
            })
        return redirect('/seaOfThieves')

    return render_template("Sea of Thieves.html",messages=messages,user=author,desc=desc,url=url)


