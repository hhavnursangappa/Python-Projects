""" Test case for registration page. """
import pytest

from HybridAutomationFramework.OpenCartV1.pageObjects.HomePage import HomePage
from HybridAutomationFramework.OpenCartV1.pageObjects.AccountRegistrationPage import AccountRegistrationPage
from HybridAutomationFramework.OpenCartV1.utilities.randomString import random_string_generator
from HybridAutomationFramework.OpenCartV1.utilities.readProperties import ReadConfig
from HybridAutomationFramework.OpenCartV1.utilities.customLogger import LogGen
import os


class Test_001_AccountReg:
    baseURL = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()  # for logging()

    @pytest.mark.regression
    def test_account_reg(self, setup):
        self.logger.info(msg="Test_001_AccountReg is started.")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.hp = HomePage(self.driver)
        self.logger.info(msg="clicking on MyAccount --> register.")
        self.hp.clickMyAccount()
        self.hp.clickRegister()

        self.logger.info(msg="clicking on MyAccount --> register.")
        self.regpage = AccountRegistrationPage(self.driver)
        self.regpage.setFirstName("John")
        self.regpage.setLastName("Canedy")

        email = random_string_generator() + '@gmail.com'
        self.regpage.setEmail(email)

        self.regpage.setTelephone("65656565")

        passw = ReadConfig.getPassword()
        self.regpage.setPassword(passw)

        self.regpage.setConfirmPassword("abcxyz")
        self.regpage.setPrivacyPolicy()
        self.regpage.clickContinue()
        self.confmsg = self.regpage.getconfirmationmsg()
        if self.confmsg == "Your Account Has Been Created!":
            self.logger.info(msg="Account registration is passed.")
            assert True
            self.driver.close()
        else:
            self.driver.save_screenshot(os.path.abspath(os.curdir) + "\\HybridAutomationFramework\\OpenCartV1\\screenshots\\" + "test_account_reg.png")
            self.logger.info(msg="Account registration is failed.")
            self.driver.close()
            assert False
