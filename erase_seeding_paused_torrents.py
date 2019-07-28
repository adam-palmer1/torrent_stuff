#!/usr/bin/python3

# Erase seeding torrents now
# Erase paused and completed torrents after 14d
# Start paused torrents

import transmissionrpc
from datetime import datetime, timedelta
from config import dl_host, dl_port, dl_user, dl_pass

def do_log(l):
    now = datetime.now()
    print("[%s] %s" % (now.strftime("%Y-%m-%d %H:%M:%S"), l))

tc = transmissionrpc.Client(dl_host, user=dl_user, password=dl_pass, port=dl_port)

for torrent in tc.get_torrents():
    if torrent.status == 'stopped':
        if torrent.progress == 100.0: #stopped and completed
            if torrent._fields['error'][0] != 0: #error field set FYI - probably data has been moved out
                pass
            if datetime.now() - torrent.date_done >= timedelta(days=14): #leave for 14 days
                tc.remove_torrent(torrent.id)
                do_log ("Removing %d" % (torrent.id,))
        else: #stopped and not completed
                do_log ("Starting incomplete %d" % (torrent.id,))
                tc.start_torrent(torrent.id)
    elif torrent.status == 'seeding' and torrent.progress == 100.0:
        do_log ("Pausing seeding torrent %d" % (torrent.id,))
        tc.stop_torrent(torrent.id)
