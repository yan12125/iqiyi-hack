import threading
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
try:
    import pyvirtualdisplay
except ImportError:
    pass

from config import PORT


class SeleniumRunner(threading.Thread):
    def __init__(self, lock, page_url):
        self.lock = lock
        self.page_url = page_url

        super(SeleniumRunner, self).__init__()

    def run(self):
        if 'pyvirtualdisplay' in globals():
            display = pyvirtualdisplay.Display()
            display.start()

        self.run_firefox()

        if 'pyvirtualdisplay' in globals():
            display.stop()

    def run_firefox(self):
        proxy = Proxy({
            'proxyType': ProxyType.PAC,
            'proxyAutoconfigUrl': 'http://localhost:%d/proxy.pac' % PORT,
        })

        driver = webdriver.Firefox(proxy=proxy)
        driver.get(self.page_url)

        print('Waiting for the proxy server')

        self.lock.acquire()

        print('Leaving...')

        driver.quit()

        self.lock.release()
