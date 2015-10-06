import urllib2
import pytest
from selenium import webdriver

browsers = {
   'firefox': webdriver.Firefox,
   'chrome': webdriver.Chrome,
}

browsers = {
   'firefox': webdriver.Firefox,
}

def pytest_addoption(parser):
   parser.addoption("--url")

def pytest_configure(config):
   global WEB_APP
   base_url = config.getoption("--url")
   WEB_APP = base_url + "planner.html"
   urllib2.urlopen(base_url + "forTestingOnly/deletedb.php").read()

@pytest.fixture(scope='session', params=browsers.keys())
def browser(request):
   driver = browsers[request.param]()
   driver.get(WEB_APP)
   driver.delete_all_cookies()
   request.addfinalizer(lambda *args: driver.quit())
   return driver

@pytest.fixture
def dpp(browser, request):
   dpp = browser
   dpp.get(WEB_APP)
   dpp.implicitly_wait(2)
   request.addfinalizer(lambda *args: dpp.delete_all_cookies())
   return dpp

