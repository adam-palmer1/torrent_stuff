#!/usr/bin/python3
import transmissionrpc
from config import dl_host, dl_port, dl_user, dl_pass


tc = transmissionrpc.Client(dl_host, user=dl_user, password=dl_pass, port=dl_port)    

