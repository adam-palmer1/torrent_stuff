#!/usr/bin/python3
from os import system, path, scandir, listdir
import PTN
import re
import datetime
from config import incoming_files, unknown_files, dest_dir, movie_files

movie_files = ["mp4", "mkv", "mpg", "avi"];
incoming_files = "/mnt/incoming"
unknown_files = "/mnt/unknown"
dest_dir = "/mnt/tv"

current_dirs = [f.path for f in scandir(dest_dir) if f.is_dir() ]

def chk_torrent(torrent_info):
    info = ['title', 'season', 'episode']
    for i in info:
        if i not in torrent_info or torrent_info[i] is '':
            print ("Unknown: %s" % (repr(torrent_info),))
            return None
    return 1

def sys_exec(command):
    now = datetime.datetime.now()
    print("[%s] %s" % (now.strftime("%Y-%m-%d %H:%M:%S"), command))
    system(command)

def sys_mkdir(full_path):
    #Do we already have this directory (case insensitive)
    for e in current_dirs:
        if e.lower() == full_path.lower():
            return e
    if not path.isdir(full_path):
        sys_command = "mkdir -p '" + full_path + "'"
        current_dirs.append(full_path)
        sys_exec(sys_command)
    return full_path

def strip_nonalnum(word):
    if not word:
        return word  # nothing to strip
    for start, c in enumerate(word):
        if c.isalnum():
            break
    for end, c in enumerate(word[::-1]):
        if c.isalnum():
            break
    return word[start:len(word) - end]

def move_unknown_file(filename):
    if '/'.join(filename.split('/')[:-1]) == incoming_files: #it's an unknown file in the root
        dest = unknown_files
    else:
        unknown_dir = "/" + '/'.join(filename.split('/')[-2:-1])
        dest = sys_mkdir(unknown_files + unknown_dir)
    sys_command = "mv " + "'" + filename + "' '" + dest + "'"
    sys_exec(sys_command)


dirs = [ incoming_files ] + [f.path for f in scandir(incoming_files) if f.is_dir() ]
for dirname in dirs:
    for filename in [f for f in listdir(dirname) if path.isfile(path.join(dirname, f))]:
        filename = dirname + "/" + filename
        file_ext = filename.split('.')[-1]
        if file_ext in movie_files:
            file_no_path = filename.split('/')[-1]
            torrent_info = PTN.parse(file_no_path)
            ok = 1
            if chk_torrent(torrent_info) is None:
                ok = 0
                #Extracting info from filename failed. Let's try the directory
                dir_no_path = filename.split('/')[-2:-1][0]
                dir_torrent_info = PTN.parse(dir_no_path)
                torrent_info = dir_torrent_info
                if chk_torrent(torrent_info) is None:
                    #move filename to unknown_files
                    move_unknown_file(filename)
                else:
                    ok = 1
            if ok == 1:
                if torrent_info['title'].find(' - ') != -1:
                    #Remove something like www.somesite.com - moviename s01...
                    torrent_info['title'] = strip_nonalnum(torrent_info['title'].split(' - ')[1]).replace(".", " ")
                #clean it up a bit now
                torrent_info['title'] = torrent_info['title'].replace("\'", " ").replace("\"", " ").replace(".", " ")
                torrent_info['title'] = re.sub(r'[^a-zA-Z0-9_ ]', '', torrent_info['title'])
                #Make sure torrent_info['title'] is still sane:
                if torrent_info['title'].strip() == '':
                    ok == 0
                    move_unknown_file(filename)
            if ok == 1:
                dest = dest_dir + "/" + torrent_info['title']
                if 'year' in torrent_info:
                    dest += " (" + str(torrent_info['year'] )+ ")"
                dest += "/" + "Season " + str(torrent_info['season']) + "/" + torrent_info['title'] + " S" + ("%.2d") % torrent_info['season'] + "E" + ("%.2d") % torrent_info['episode'] + "." + file_ext
                #mkdir the location
                dest = sys_mkdir( "/".join(dest.split("/")[0:-1]) )
                sys_command = "mv " + "'" + filename + "' '" + dest + "'"
                sys_exec(sys_command)
    if dirname is not incoming_files: #don't delete the root
        sys_command = "rm -rf '" + str(dirname) + "'"
        sys_exec(sys_command)
