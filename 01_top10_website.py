#!/usr/bin/env python

from selenium import webdriver
import time


def get_top10_website(source=''):
    url_candidate = []
    if source.lower() == 'alex':
        pass
    else:
        url_candidate = ['google.com',
                         'youtube.com',
                         'facebook.com',
                         'baidu.com',
                         'yahoo.com',
                         'amazon.com',
                         'wikipedia.org',
                         'qq.com',
                         'twitter.com',
                         'live.com',
                         ]
    return url_candidate


if __name__ == '__main__':
    url_candidate = get_top10_website()
    driver = webdriver.Firefox()
    offset = 1
    for url in url_candidate:
        target_url = 'http://' + url + '/'
        filename = '%02d.' % offset + url + '.png'
        print "open url %s" % target_url
        driver.get(target_url)
        driver.save_screenshot(filename)
        offset += 1
    driver.close()
    driver.quit()
