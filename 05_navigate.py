from selenium import webdriver
from time import sleep

uri = ["www.google.com", "www.yahoo.com", "www.bbc.com", "www.w3schools.com"]
# selenium.common.exceptions.WebDriverException: Message: Reached error page: about:certerror


def get_path(base):
    return base + ".png"


if __name__ == "__main__":
    firefox = webdriver.Firefox()
    for target in uri:
        url = "https://" + target
        firefox.get(url)
        print firefox.title
        firefox.save_screenshot(get_path(target))
    for i in xrange(len(uri)):
        firefox.back()
        sleep(1)
        firefox.refresh()
        sleep(1)
        print i, firefox.title
    target = uri[-1]
    url = 'https://' + target
    firefox.set_window_size(800, 600)
    firefox.get(url)
    firefox.save_screenshot(get_path(target + '_800x600'))
    firefox.set_window_size(1024, 768)
    firefox.save_screenshot(get_path(target + '_1024x768'))
    firefox.maximize_window()
    firefox.save_screenshot(get_path(target + '_max'))
    firefox.close()
    firefox.quit()
