#crawler from http://konachan.net/

"""
Copyright (C) 2018 by
urayoru <v3691261@gmail.com>
All rights reserved.
BSD license.
github: http://github.com/urayoru113.
"""


import requests
import os
import time
import multiprocessing as mult
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup

save_dir = './image_doo'
total_img = 108082
def downloader(url):
    global total_img
    r = False
    url = "http:" + url
    filepath = save_dir + '/' + url.split('/')[-1]
    if os.path.exists(filepath):
        print("File %s already exist. Try to download next image......" %filepath)
        total_img += 1
        return
    while not r or r.status_code != 200:
        try:
            r = requests.get(url, stream=True, timeout=10)
        except requests.exceptions.RequestException as e:
            print("%s connect failed! when is downloading" %url)
            continue
        try:
            with open(filepath, 'wb') as f: 
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            print('Download success. Save file to %s' %filepath)
            total_img += 1
            return
        except KeyboardInterrupt:
            if os.path.exists(filepath):
                os.remove(filepath)
            print("Keyboard interrupt")
            raise KeyboardInterrupt
            os._exit(0)
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            print("From %s" %url)
            print(e)
    else:
        
        return True

def main():
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    mult.freeze_support()
    pool = ThreadPool(mult.cpu_count())
    page = 7352
    while page <= 9948:
        url = 'http://konachan.net/post?page=%d&tags=' %page
        request = False
        imgs_url = []
        while not request or request.status_code != 200:
            try:
                request = requests.get(url, timeout=10)
            except requests.exceptions.RequestException:
                print("html code: %d" % request.status_code)
                print("Connect reject by %s" %url)
                print("wait 10 sec to keep connecting......")
                time.sleep(10)
        soup = BeautifulSoup(request.text, 'html.parser')
        soup_post = soup.find(id='post-list-posts')
        if not soup_post:
            print("Doesn't search any image in this page")
            page += 1
            continue
        print("Download form %s" %url)
        for img in soup.find_all('img', class_='preview'):
            imgs_url.append(img['src'])
        pool.map(downloader, imgs_url)
        page += 1
        print("total image %d" %total_img)
    pool.close()
    pool.join()
        

if __name__ == '__main__':
    main()