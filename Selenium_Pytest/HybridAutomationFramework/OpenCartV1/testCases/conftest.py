""" Script to add fixtures. """

import pytest
import os
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture()
def setup(browser):
	match browser:
		case 'edge':
			driver = webdriver.Chrome(EdgeChromiumDriverManager().install())
		case 'chrome':
			driver = webdriver.Chrome(ChromeDriverManager().install())
		case 'firefox':
			driver = webdriver.Chrome(GeckoDriverManager().install())
		case _:
			driver = webdriver.Chrome(ChromeDriverManager().install())

	print(f"Launching {browser} browser")
	return driver


def pytest_add_option(parser):
	parser.add_option('--browser')


@pytest.fixture()
def browser(request):
	return request.config.get_option('--browser')


# ########## pytest HTML Report ################
# It is hook for Adding Environment info to HTML Report
def pytest_configure(config):
	config._metadata['Project Name'] = 'Opencart'
	config._metadata['Module Name'] = 'CustRegistration'
	config._metadata['Tester'] = 'Pavan'


# It is hook for delete/Modify Environment info to HTML Report
@pytest.mark.optionalhook
def pytest_metadata(metadata):
	metadata.pop("JAVA_HOME", None)
	metadata.pop("Plugins", None)


# Specifying report folder location and save report with timestamp
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
	config.option.htmlpath = os.path.abspath(os.curdir)+"\\reports\\"+datetime.now().strftime("%d-%m-%Y %H-%M-%S")+".html"
