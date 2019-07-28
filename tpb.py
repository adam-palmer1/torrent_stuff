#!/usr/bin/python3

import requests
import re
from time import sleep
from os import path
from config import tpb, headers, page_max, page_retries, db
from scraper import scrape
from config import dl_host, dl_port, dl_user, dl_pass
import transmissionrpc

#----#

#global transmission object
tc = transmissionrpc.Client(dl_host, user=dl_user, password=dl_pass, port=dl_port)

def get_torrents():
    session = requests.Session()
    session.headers.update(headers)
    entries = []

    for p in range(page_max):
        url = tpb + '/browse/200/' + str(p) + '/7'
        for t in range(page_retries):
            page = session.get(url)
            if page.status_code is not 200:
                print ("Error %d retrieving page %d (retry %d): " % (page.status_code, p, t))
                sleep(t)
            else:
                break #break out of retry loop
        if page.status_code is not 200:
            #We exhausted the retries and it's still no good
            break #break out of this page loop
        entries += scrape(page.text)
    return entries

def parse_torrents(entries):
    entries_seen = []
    downloads = []
    if path.isfile(db):
        with open(db, 'r') as content:
            entries_seen = content.read().split("\n")

    for entry in entries:
        entry_info = entry['entry_info']
        unique_identifier = re.sub(r'[^a-zA-Z0-9]', '', entry_info['title'])
        clean_name = re.sub(r'[^a-zA-Z0-9_. ]','',entry['entry_name'])
        if 'season' in entry_info and 'episode' in entry_info:
            #series
            unique_identifier += str(entry_info['season']) + str(entry_info['episode'])
        if unique_identifier not in entries_seen:
            entries_seen.append(unique_identifier)
            i = input("Download %s [y/N]? " % entry['entry_name'])
            if i.lower() in ["y", "yes"]:
                downloads.append( (entry['entry_name'], entry['entry_link']) )

    f = open(db, "w")
    f.write("\n".join(entries_seen))
    f.close()
    return downloads


if __name__ == "__main__":
    print ("Getting torrent list...")
    t = get_torrents()
    print ("Parsing torrents...")
    for torrent in parse_torrents(t):
        print("Adding %s" % (torrent[0],))
        t = tc.add_torrent(torrent[1])
