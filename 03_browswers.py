from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import time
import unittest

# http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html

def let_me_google_it_for_you(browser, url, sentence):
    browser.get(url)
    time.sleep(1)
    str_title = browser.title
    print repr(str_title)
    if str_title.lower().find("google") < 0:
        return False
    try:
        elem = browser.find_element_by_id('lst-ib') # //*[@id="lst-ib"]
        # //*[@id="resultStats"]
        elem.send_keys(sentence + Keys.RETURN)
        time.sleep(1)
        elem = browser.find_element_by_id('resultStats')
        print elem.text
        # div.g:nth-child(1) > div:nth-child(1)
        css = "div.g:nth-child(1) > div:nth-child(1)"
        elem = browser.find_element_by_css_selector(css)
        print repr(elem.text.split('\n')[0])
    except NoSuchElementException as err:
        print "Oops, web element is not found"
        print err.msg
        print err.stacktrace
        return False
    except NoSuchWindowException as err:
        print "Oops, webdrive or browser error"
        print err.msg
        print err.stacktrace
        return False
    return True


class BrowswerCompatibilityTestCase(unittest.TestCase):

    def setUp(self):
        self.sentence = "the best browser in the world"
        self.url = "https://www.google.com.tw"
        self.browser = None

    def tearDown(self):
        if self.browser:
            self.browser.close()
            self.browser.quit()

    def testFirefox(self):
        """Mozilla Firefox"""
        firefox = webdriver.Firefox()
        self.assertTrue(let_me_google_it_for_you(firefox,
                                                 self.url, self.sentence))
        self.browser = firefox

    def testChrome(self):
        """Google Chrome"""
        chrome = webdriver.Chrome()
        self.assertTrue(let_me_google_it_for_you(chrome,
                                                 self.url, self.sentence))
        self.browser = chrome

    def testIE(self):
        """Microsoft IE"""
        ie = webdriver.Ie()
        self.assertTrue(let_me_google_it_for_you(ie,
                                                 self.url, self.sentence))
        self.browser = ie

    def testEdge(self):
        """Microsoft Edge"""
        edge = webdriver.Edge()
        self.assertTrue(let_me_google_it_for_you(edge,
                                                 self.url, self.sentence))
        self.browser = edge


if __name__ == '__main__':
    unittest.main(verbosity=2)
