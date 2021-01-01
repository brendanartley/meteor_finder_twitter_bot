import tweepy
import time
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd
from math import cos, asin, sqrt

#The next four variables are all spceific to each twitter users account, and you can generate these codes for your account at developer.twitter.com

CONSUMER_KEY = '######'
CONSUMER_SECRET = '#####'
ACCESS_KEY = '#####'
ACCESS_SECRET = '######'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

#meteor_data

m_landings = pd.read_csv('/Users/brendanartley/Desktop/code/twitterbot/meteorite_landings.csv')
m_landings = m_landings.loc[m_landings.latitude!=0]
m_landings = m_landings.loc[m_landings.longitude!=0]
m_landings = m_landings.dropna(subset=['latitude','longitude'])

def get_me_the_meteor(my_lat, my_long, last_seen_text, m_landings):
    closest_dist = None
    for coor in m_landings[['latitude','longitude','id']].values:
        p = 0.017453292519943295  #Pi/180
        a = 0.5 - cos((coor[0]-my_lat)*p)/2 + cos(my_lat*p)*cos(coor[0]*p) * (1-cos((coor[1]-my_long)*p)) / 2
        dist = 12742 * asin(sqrt(a)) #12742 is the 2*r radius of the earth in km
        if closest_dist is not None:
            if dist<closest_dist:
                closest_dist = dist
                closest_id = coor[2]
            else:
                continue
        else:
            closest_dist = dist
            closest_id = coor[2]

    closest_dist = round(closest_dist, 1)
    closest_id = closest_id.astype(int)
    closest_lat = m_landings.loc[m_landings.id==closest_id]['latitude'].values[0]
    closest_long = m_landings.loc[m_landings.id==closest_id]['longitude'].values[0]
    #maps_link = 'https://www.google.com/maps/dir/{},{}/'.format(closest_lat, closest_long)
    maps_link = 'https://www.google.com/maps/search/?api=1&query={},{}'.format(closest_lat, closest_long)

    closest_row = m_landings.loc[m_landings.id==closest_id]
    closest_location = closest_row['location'].values[0]
    closest_year = closest_row['year'].values[0].astype(int).astype(str)
    closest_meteor_name = closest_row['meteorite_name'].values[0]
    return(maps_link, closest_year, closest_location, closest_meteor_name)

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    #using tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions): #reversed as we read through the oldest tweets first
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        last_seen_text = mention.full_text
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#meteorfinder' in mention.full_text.lower():
            print('found #meteorfinder!', flush=True)
            print('responding back...', flush=True)
            geolocator = Nominatim(user_agent="myGeocoder")
            last_seen_text = last_seen_text.rsplit(' ', 1)[0].rsplit(' ', 1)[1] #removing the hastag and @reply from string
            location = geolocator.geocode(last_seen_text)
            try:
                maps_link, closest_year, closest_location, closest_meteor_name = get_me_the_meteor(location.latitude, location.longitude, last_seen_text, m_landings)
                api.update_status('@' + mention.user.screen_name + ' The closest meteor know meteor site to you is called The {} Meteor which landed in {} in {}. Go check it out!'.format(closest_meteor_name, closest_location, closest_year) + maps_link, mention.id)
            except:
                api.update_status('@' + mention.user.screen_name + ' Sorry I either do not recognize that place, or I can not understand the format of your tweet! Check my bio for a meteor finder example!', mention.id)

while True:
    reply_to_tweets()
    time.sleep(15)
