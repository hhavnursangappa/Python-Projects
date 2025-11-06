import pytest

from HybridAutomationFramework.OpenCartV1.pageObjects.HomePage import HomePage
from HybridAutomationFramework.OpenCartV1.pageObjects.LoginPage import LoginPage
from HybridAutomationFramework.OpenCartV1.utilities.readProperties import ReadConfig
from HybridAutomationFramework.OpenCartV1.utilities.customLogger import LogGen
import os


class Test_Login:
    baseURL = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()  # Logger

    user = ReadConfig.getUseremail()
    password = ReadConfig.getPassword()

    @pytest.mark.sanity
    def test_login(self, setup):
        self.logger.info("******* Starting test_002_login **********")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.hp = HomePage(self.driver)
        self.hp.clickMyAccount()
        self.hp.clickLogin()

        self.lp = LoginPage(self.driver)
        self.lp.setEmail(self.user)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()

        self.targetpage = self.lp.isMyAccountPageExists()
        if self.targetpage is True:
            assert True
        else:
            self.driver.save_screenshot(os.path.abspath(os.curdir) + "\\screenshots\\" + "test_login")
            assert False

        self.driver.close()
        self.logger.info("******* End of test_002_login **********")
