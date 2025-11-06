import pytest
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


@pytest.fixture()
def setup(browser):
    if browser=='edge':
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        print("Launching Edge browser.........")
    elif browser=='firefox':
        driver = webdriver.Firefox(GeckoDriverManager().install())
        print("Launching firefox browser.........")
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        print("Launching chrome browser.........")
    return driver

def pytest_addoption(parser):    # This will get the value from CLI /hooks
    parser.addoption("--browser")

@pytest.fixture()
def browser(request):  # This will return the Browser value to setup method
    return request.config.getoption("--browser")