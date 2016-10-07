import random
import string
import sys
import urllib2
import os
import re
from urlparse import urlparse

def page_loader(url_name, dir_name='imgs'):

    page_to_open = urllib2.urlopen(url_name)
    target_page = page_to_open.read()
    base_dir = os.path.dirname(os.path.realpath(__file__))
    dir_to_save = os.path.join(base_dir, dir_name)
    new_file_name = '%s.html' % ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(10))
    if not os.path.exists(dir_to_save):
        os.makedirs(dir_to_save)


    images_on_page = re.findall('link .*?href="(.*?)"', target_page)
    internal_images = [img for img in images_on_page if img.startswith('/')]
    external_images = [img for img in images_on_page if not img.startswith('/')]

    for image in internal_images:
        image_url = '%s%s' % (page_to_open.geturl()[:-1], image)
        new_image_name = urlparse(image_url).path.split('/')[-1]
        with open(os.path.join(dir_to_save, new_image_name), 'w') as new_image:
            new_image.write(urllib2.urlopen(image_url).read())
            target_page = re.sub(image, new_image.name, target_page)

    for image_url in external_images:
        new_image_name = urlparse(image_url).path.split('/')[-1]
        with open(os.path.join(dir_to_save, new_image_name), 'w') as new_image:
            new_image.write(urllib2.urlopen(image_url).read())
            target_page = re.sub(image_url, new_image.name, target_page)

    with open(os.path.join(base_dir, new_file_name), 'w') as new_file:
        new_file.write(target_page)

if __name__ == '__main__':
    target_url = 'http://www.axa-direct.co.jp/'
    if len(sys.argv) > 2:
        dir_name = './Downloads/'
        page_loader(target_url, dir_name)
    else:
        page_loader(target_url)
