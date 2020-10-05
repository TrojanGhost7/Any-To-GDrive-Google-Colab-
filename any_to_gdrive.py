# -*- coding: utf-8 -*-
"""Any To GDrive.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cIziKBmiO1BxE018zSPGwlPRzncUgEEl

# Mount Drive

Mount or Unmount your Gdrive...
"""

#@markdown <br><center><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Google_Drive_logo.png/600px-Google_Drive_logo.png' height="50" alt="Gdrive-logo"/></center>
#@markdown <center><h3>Mount Gdrive</h3></center><br>
MODE = "MOUNT" #@param ["MOUNT", "UNMOUNT"]
#Mount your Gdrive! 
from google.colab import drive
drive.mount._DEBUG = False
if MODE == "MOUNT":
  drive.mount('/content/drive', force_remount=True)
elif MODE == "UNMOUNT":
  try:
    drive.flush_and_unmount()
  except ValueError:
    pass
  get_ipython().system_raw("rm -rf /root/.config/Google/DriveFS")

"""# URL Download

Just paste the URL of the file you want to download & the path where you want to save it...
"""

#@markdown <br><center><h3>URL Downloader</center></h3><br>
import os
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
URL = "" #@param {type : "string"}
PATH = "" #@param {type:"string"}
os.chdir(PATH)
try:  
  !wget -c {URL} --no-check-certificate
except FileNotFoundError:
  print("""
  The Given Path does not exist...
  Please Check The Path...
  """)

"""# Torrent Download

**If you have .torrent file convert it to magnet by using the website [torrent2magnet.com](https://)**
"""

#@markdown <br><center><h3>Run this before using torrents<h3><center><br>
!apt install python3-libtorrent

#@markdown <br><center><h3>Torrent Downloader</center></h3><br>
import libtorrent as lt
import time
import datetime

MAGNET = "" #@param {type : "string"}
PATH = '' #@param {type : "string"}

ses = lt.session()
ses.listen_on(6881, 6891)
params = {
    'save_path': PATH,
    'storage_mode': lt.storage_mode_t(2),
    'paused': False,
    'auto_managed': True,
    'duplicate_is_error': True}
link = MAGNET
print(link)

handle = lt.add_magnet_uri(ses, link, params)
ses.start_dht()

begin = time.time()
print(datetime.datetime.now())

print ('Downloading Metadata...')
while (not handle.has_metadata()):
    time.sleep(1)
print ('Got Metadata, Starting Torrent Download...')

print("Starting", handle.name())

while (handle.status().state != lt.torrent_status.seeding):
    s = handle.status()
    state_str = ['queued', 'checking', 'downloading metadata', \
            'downloading', 'finished', 'seeding', 'allocating']
    print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))
    time.sleep(5)

end = time.time()
print(handle.name(), "COMPLETE")

print("Elapsed Time: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")

print(datetime.datetime.now())