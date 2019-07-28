#!/usr/bin/python3

import subprocess
import requests
import re
from time import sleep
from os import path
import multiprocessing
from urllib import parse
from sys import argv
from config import tpb, headers, page_retries
from scraper import scrape
from config import dl_host, dl_port, dl_user, dl_pass
import transmissionrpc

#----#

#global transmission object
tc = transmissionrpc.Client(dl_host, user=dl_user, password=dl_pass, port=dl_port)

def get_torrents(url):
    session = requests.Session()
    session.headers.update(headers)
    entries = []

    for t in range(page_retries):
        page = session.get(url)
        if page.status_code is not 200:
            print ("Error retrieving page: %d (Retrying in %d seconds)" % (page.status_code, t))
            sleep(t)
        else:
            break #break out of retry loop

    if page.status_code is not 200:
        #We exhausted the retries and it's still no good
        print("Error performing search")
        quit()

    return scrape(page.text)

if __name__ == "__main__":
    if len(argv) < 2:
        print("Provide a search query")
        quit()

    search = parse.quote(" ".join(argv[1:]))
    url = tpb + "/search/" + search + "/0/99/0"

    print ("Getting torrent list...")
    t = get_torrents(url)
    n = 0
    for i in t:
        print(str(n) + ">\t(" + i['entry_seeds'] + "/" + i['entry_leech'] + ") " + i['entry_name'])
        n += 1

    if not t:
        print ("No torrents found!")
        quit()

    passed = 0
    magnets = []
    while passed is 0:
        n = input("Download (q to quit, ',' for multiple)? ")
        if n.lower() == "q":
            quit()

        try:
            for i in n.split(","):
                magnets.append( (t[int(i)]['entry_link'], t[int(i)]['entry_name']) )
            passed = 1
        except Exception as e:
            print(e)

    for magnet in magnets:
        t = tc.add_torrent(magnet[0])
        print("Queued %s" % (magnet[1],))
