#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import sys
import time
import datetime
import shutil
import codecs


CONST_PATH_NAME = 'storage'


def get_pwd():
    return os.path.split(sys.argv[0])[0]


def get_date_string():
    str_date = datetime.datetime.now().strftime("%Y-%m%d-%H%M")
    return str_date


def prepare_storage_folder():
    target_path = os.path.join(get_pwd(), CONST_PATH_NAME, get_date_string())
    if not os.path.isdir(target_path):
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        os.makedirs(target_path)
    return target_path


def prepare_child_folder(root, child):
    target_path = os.path.join(root, child)
    if not os.path.isdir(target_path):
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        os.makedirs(target_path)
    return target_path


def byebye(message):
    print "last note: %s" % message
    sys.exit(-1)


def setup_webdriver():
    driver = webdriver.Firefox()
    driver.set_window_size(1024, 1240)
    return driver


def open_url_take_screenshot_and_html(urls, folder):
    folder_png = prepare_child_folder(folder, "png")
    folder_htm = prepare_child_folder(folder, "htm")
    worker = webdriver.Firefox()
    for url in urls:
        print "url2go: %s" % url
        target_id = os.path.split(url)[-1]
        # open page
        worker.get(url)
        # store screenshot
        worker.save_screenshot(os.path.join(folder_png, target_id + ".png"))
        html_path = os.path.join(folder_htm, target_id + ".html")
        # with open(html_path, "wb", encoding='utf-8') as writer:
        with codecs.open(html_path, "w", encoding='utf-8') as writer:
            writer.write(worker.page_source)
    worker.close()
    worker.quit()


def do_something(driver, storage):
    driver.get("http://24h.pchome.com.tw/")
    # step 1: make sure homepage is ready
    driver.save_screenshot(os.path.join(storage, "1_Homepage.png"))
    if "PChome 24h" not in driver.title:
        byebye("oops" + repr(driver.title))
    # step 2: go to 3C
    # OnSaleContainer
    target = driver.find_element_by_id("OnSaleContainer")
    if not target:
        byebye("oops" + "not find element named OnSaleContainer")
    target.click()
    time.sleep(5)
    driver.save_screenshot(os.path.join(storage, "2_OnSale.png"))

    for topic in ("block_3c", "block_ce", "block_food"):
        target = driver.find_element_by_id(topic)
        if not target:
            byebye("oops" + "not find element named %s" % topic)
        # step 3: collect interesting page under every child of topic
        interests = []
        for children in driver.find_elements_by_xpath("//div[@id='%s']" % topic):
            # actually, it supposed has one named as topic
            for the_one in children.find_elements_by_css_selector("div.body a"):
                data = the_one.get_attribute("href")
                if data and len(data):
                    interests.append(data)
        page_folder = prepare_child_folder(storage, topic)
        open_url_take_screenshot_and_html(interests, page_folder)


def cleanup_webdriver(driver):
    driver.close()
    driver.quit()


if __name__ == '__main__':
    storage_path = prepare_storage_folder()
    web_driver = setup_webdriver()
    do_something(web_driver, storage_path)
    cleanup_webdriver(web_driver)

