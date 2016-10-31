from __future__ import print_function,unicode_literals
from bs4 import BeautifulSoup as BS
import youtube_dl
import time
import argparse
import logging
import json
import praw
import pychromecast
import re
import urllib2
import requests as r
from urllib2 import Request, urlopen, URLError,urlopen


def main():
    parser = argparse.ArgumentParser(description='Welcome to Jacurutu. The Spice must flow.')
    parser.add_argument("command", help="enter command here")
    parser.add_argument("search_string")
    parser.add_argument("-e", "--episode", help='Pick an episode', type=int)
    parser.add_argument("-s", "--season", help='Pick a season', type=int)
    parser.add_argument("-ip",help='IP Address of Chromecast', type=str)
    parser.add_argument("-url",help="URL of embedded video", type=str)

    args = parser.parse_args()
    if args.command == "search":
        if args.episode:
            find_episode(args.search_string, args.season, args.episode)
    if args.command == "casturl":
        print(args.search_string)
        chromecast(args.search_string)
    if args.command == "redditstream":
        get_reddit_instance(args.search_string)
    elif args.command == "cast":
        count = 0
        cast_links(find_episode(args.search_string, args.season, args.episode))
        p = re.compile(r'.*UID(\d+)')
        with open('./links.txt') as infile:
            for line in infile:
                if count == 0:
                    chromecast(line)
                    count == 1
                response = raw_input("Try next link?  (type 'yes')")
                if response == "yes":
                    chromecast(line)
                else:
                    quit()

def cast_links(links):
    count = 0
    p = re.compile(r'.*UID(\d+)')
    unsupported = 'playedto.me'
    with open('./links.txt') as infile:
         for line in infile:
             if "http://vodlocker.com" in line:
                 if count == 0:
                     chromecast(line)
                     count == 1
                 response = raw_input("Try next link? (type 'yes')" )
                 if response =="yes":
                     chromecast(line)
                 else:
                     quit()
def chromecast(url):
    options = {
            'format': 'bestvideo/best',
            'videoformat' : "mp4",
    }
    if 'paypal' in url:
        quit()
    if 'twitter' in url:
        quit()
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    with ydl:
            result = ydl.extract_info(url, download=False)

            if 'paypal' in result:
                quit()
            if 'shop' in result:
                quit()
            if 'entries' in result:
                # Can be a playlist or a list of videos
                video = result['entries'][0]
            else:
                # Just a video
                video = result
                s = str(v)
                if "paypal" in s:
                    quit()
                if "shoppingcart" in s:
                    quit()

    if video == "":
        quit()
    video_url = video['url']
    cast_list = pychromecast.get_chromecasts_as_dict().keys()
    try_cast = raw_input("Castable link found. Type 'yes' to cast it")
    if try_cast != "yes":
        quit()
    print("Select a chromecast:")
    for chromecast in cast_list:
        response = raw_input("%s? (type 'yes') " % str(chromecast))
        if response == "yes":
            cast_name = str(chromecast)
            break
    cast = pychromecast.get_chromecast(friendly_name=cast_name)
    cast.wait()
   # print(cast.device)
   # print(cast.status)
    mc = cast.media_controller
    mc.play_media(video_url, 'video/mp4')
   # print(mc.status)
    #link = soup.find(type="video/mp4")
    #print(link)
    #links = [link.get('href') for link in soup.find_all('a')]
    #videos = []
    #for link in links:
    #   print(link)
    #   if isinstance(link, str):
    #      match = re.search('.mp4',link)
    #      print(match)
    #mc.play_media(url, 'video/html')
    #mc.play_media('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')
    #print(mc.status)
def find_episode(show, ssn, epi):
    f3=open('./links.txt','w+')
    from primewire.primewire import search
    print(search(show,year=None,season=ssn,episode=epi),file=f3)

def get_reddit_instance(sub):
    my_user_agent = "my user agent"
    my_client_id = "q3941h84H3Sytg"
    my_client_secret = "LF6xUjrTOI7NZGdfG-Fh2L--8-A"
    my_username = ""
    my_password = ""
    reddit = praw.Reddit(user_agent=my_user_agent,
                         client_id=my_client_id,
                         client_secret=my_client_secret,
                         username=my_username,
                         password=my_password)
    f3 = open('./links.txt','w+')
    count = 0
    response = raw_input("What team are you looking for?")
    quality = raw_input("Quality?")
    for submission in reddit.subreddit(sub).hot(limit=30):
        if response in submission.title:
            submission.comments.replace_more(limit=0)
            for top_level_comment in submission.comments:
                if quality == "":
                    if "HQ" in top_level_comment.body:
                        print("Trying HQ...")
                    if "HD" in top_level_comment.body:
                        print("Trying HD...")
                    if "SD" in top_level_comment.body:
                        print("Trying SD...")
                    if "Mobile" in top_level_comment.body:
                        print("Trying Mobile...")
                    if "720p" in top_level_comment.body:
                        split_url = re.findall(r'\((.*?)\)', top_level_comment.body)
                    else:
                        print("Quality Unknown. Trying...")
                    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', top_level_comment.body)
                    if "720p" not in top_level_comment.body:
                        Cast_Other(url)
                    if "720p" in top_level_comment.body:
                        Cast_720p(split_url)
                elif quality in top_level_comment.body:
                    if quality == "720p":
                        split_url = re.findall(r'\((.*?)\)', top_level_comment.body)
                        Cast_720p(split_url)
                    else:
                        print("Trying " + quality + "...")
                        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', top_level_comment.body)
                        Cast_Other(url)

def Cast_720p(split_url):
    print("Trying 720p...")
    string_url = str(split_url)
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string_url)
    for x in url:
        y = str(x)
        s = str.replace(y,"',","")
        z = str(s)
        q = str.replace(z,"']","")
        g = str(q)
        cast_url = g.splitlines()
        for line in cast_url:
            try:
                chromecast(line)
            except:
                pass

def Cast_Other(url):
    for x in url:
        y = str(x)
        s = str.replace(y,"/)","")
        z = str(s)
        q = str.replace(z,")","")
        print(q)
        try:
            chromecast(q)
        except:
            pass



if __name__ == '__main__':
    main()


