from __future__ import print_function
from bs4 import BeautifulSoup
import time
import argparse
import logging
import json
import pychromecast
import re
import urllib2
from urllib2 import Request, urlopen, URLError,urlopen


def main():
    parser = argparse.ArgumentParser(description='Welcome to Jacurutu. The Spice must flow.')
    parser.add_argument("command", help="enter command here")
    parser.add_argument("search_string")
    parser.add_argument("-e", "--episode", help='Pick an episode', type=int)
    parser.add_argument("-s", "--season", help='Pick a season', type=int)
    parser.add_argument("-ip",help='IP Address of Chromecast', type=str)

    args = parser.parse_args()
    if args.command == "search":
        if args.episode:
            find_episode(args.search_string, args.season, args.episode)
        else:
            x=2#print search(args.search_string)
    elif args.command == "cast":
            count = 0
            cast_links(find_episode(args.search_string, args.season, args.episode))
	    p = re.compile(r'.*UID(\d+)')
	    with open('./links') as infile:
                 for line in infile:
                       if count == 0:
                          chromecast(line)
                          count == 1
                       response=raw_input('Try next link?')
                       if response == "yes":
                          chromecast(line)
                       else:
                         quit()
     											

def cast_links(links):
    link_json = json.loads(links)
    f1=open('./links','w+')
    sources = link_json['sources']
    for link in sources:
	if link['name'] == "vidzi.tv":
           url = link['url']
           print(url,file=f1)
        else:
           urf = "http://www." + link['name']+ link['url'] 

def chromecast(url):
    pychromecast.get_chromecasts_as_dict().keys()
    ['Caladan']
    cast = pychromecast.Chromecast('192.168.1.9')
    cast.wait()
    print(cast.device)
    print(cast.status)
    mc = cast.media_controller
    print(url)
    cheat='http://www.vodlocker.com/qrse9x350sy1'
    soup = BeautifulSoup(urlopen(cheat),"lxml")
    links = [link.get('href') for link in soup.find_all('a')]
    videos = []
    for link in links:
       print(link)
       if isinstance(link, str): 
          match = re.search('.mp4',link)
          print(match)
    mc.play_media(url, 'video/html')
    #mc.play_media('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')
    #print(mc.status)
    
def search(string):
    request = Request('http://ptvapi.com/api?q=%s' % string)
    response = urlopen(request)
    shows = response.read()
    return shows

def find_episode(show, season, episode):
    request = Request('http://ptvapi.com/api?n=%s&s=%d&e=%d&f' % (show, season, episode))
    response = urlopen(request)
    links = response.read()
    return links

if __name__ == '__main__':
    main()


