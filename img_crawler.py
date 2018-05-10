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
from bs4 import BeautifulSoup

def downloader(url, filepath):
    
    if os.path.exists(filepath):
        print("File %s already exist. Try to download next image......" %filepath)
        return False
    try:
        r = requests.get(url, stream=True, timeout=10)
    except requests.exceptions.RequestException as e:
        print("%s connect failed!" %url)
        return True
    if r.status_code == 200:
        try:
            with open(filepath, 'wb') as f: 
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            print('Download success. Save file to %s' %filepath)
            return False
        except KeyboardInterrupt:
            if os.path.exists(filepath):
                os.remove(filepath)
            print("Keyboard interrupt")
            raise KeyboardInterrupt
            os._exit(0)
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            print("Unknow exception")
            return True
    else:
        print("Connect failed when is downloading")
        return True


def main():
    if not os.path.isdir('image'):
        os.makedirs('image')
    
    total_img = 104509
    for i in range(7133, 9945):
        filename = 1
        url = 'http://konachan.net/post?page=%d&tags=' %i
        request = False
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
            print("Finished download all image")
            os._exit(0)
        print("Download form %s" %url)
        for img in soup.find_all('img', class_='preview'):
            filepath = './image/' + str(i) + '_' + str(filename) + '.jpg'
            if os.path.exists(filepath):
                print("File %s already exist. Try to download next image......" %filepath)
                total_img += 1
                filename += 1
                continue
            ret = downloader("http:" + img['src'], filepath)
            if ret:
                print("Download failed")
                print("wait 10 sec to keep downloading......")
                time.sleep(10)
                while downloader("http:" + img['src'], filepath):
                    print("wait 10 sec to keep downloading......")
                    time.sleep(10)
                total_img += 1
                filename += 1
            else:
                total_img += 1
                filename += 1
        print("total image %d" %total_img)

if __name__ == '__main__':
    main()