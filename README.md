A variety of Python tools for interacting with TPB, scraping and downloading torrents.

Magnet links are passed via RPC to a Transmission server for downloading.

download.sh: Download a torrent with transmission-cli and kill when complete
tpb.py: Get all new torrents since last script run from TPB and prompt for download
tpb_search.py: Search TPB for a torrent
transmission_rpc_gettorrent.py: How to connect to Transmission RPC via Python
erase_seeding_paused_torrents.py: Cron job to clean up Transmission server torrents via RPC
move_incoming_torrents.py: Cron job to classify new TV series torrents in /mnt/incoming using PTN module and move them to the right place. 

settings.json: Transmission RPC settings

config.py:
```tpb = 'https://tpbprox.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

page_max = 5
page_retries = 5

db = '/home/adam/code/torrent_downloader/db.txt'
# A list of anything to highlight if it appears
waiting_list = '/home/adam/code/torrent_downloader/waiting.txt'

#transmission rpc server
dl_host=""
dl_port=""
dl_user=""
dl_pass=""

movie_files = ["mp4", "mkv", "mpg", "avi"];
incoming_files = "/mnt/incoming"
unknown_files = "/mnt/unknown"
dest_dir = "/mnt/tv"

#ssl verification
verify = False
```
