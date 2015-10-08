import threading
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

from config import PORT, PAGE_URL


class SeleniumRunner(threading.Thread):
    def __init__(self, lock):
        self.lock = lock

        super(SeleniumRunner, self).__init__()

    def run(self):
        proxy = Proxy({
            'proxyType': ProxyType.PAC,
            'proxyAutoconfigUrl': 'http://localhost:%d/proxy.pac' % PORT,
        })

        driver = webdriver.Firefox(proxy=proxy)
        driver.get(PAGE_URL)

        print('Waiting for the proxy server')

        self.lock.acquire()

        print('Leaving...')

        driver.quit()

        self.lock.release()
