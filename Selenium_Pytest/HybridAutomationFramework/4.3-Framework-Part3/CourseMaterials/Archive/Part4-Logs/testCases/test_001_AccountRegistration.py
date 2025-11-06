from pageObjects.HomePage import HomePage
from pageObjects.AccountRegistrationPage import AccountRegistrationPage
from utilities import randomeString
import os
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen


class Test_001_AccountReg:
    baseURL = ReadConfig.getApplicationURL()
    logger=LogGen.loggen() # for logging

    def test_account_reg(self,setup):
        self.logger.info("**** test_001_AccountRegistration started *** ")
        self.driver = setup
        self.driver.get(self.baseURL)
        self.logger.info("Launching application")
        self.driver.maximize_window()

        self.hp=HomePage(self.driver)
        self.logger.info("clicking on MyAccount--> register")
        self.hp.clickMyAccount()
        self.hp.clickRegister()

        self.logger.info("Proving customer details for registration")
        self.regpage=AccountRegistrationPage(self.driver)
        self.regpage.setFirstName("John")
        self.regpage.setLastName("Canedy")
        self.email=randomeString.random_string_generator()+'@gmail.com'
        self.regpage.setEmail(self.email)
        self.regpage.setTelephone("65656565")
        self.regpage.setPassword("abcxyz")
        self.regpage.setConfirmPassword("abcxyz")
        self.regpage.setPrivacyPolicy()
        self.regpage.clickContinue()
        self.confmsg=self.regpage.getconfirmationmsg()
        if self.confmsg=="Your Account Has Been Created!":
            self.logger.info("Account registration is passed..")
            assert True
            self.driver.close()
        else:
            self.driver.save_screenshot(os.path.abspath(os.curdir)+"\\screenshots\\"+"test_account_reg.png")
            self.logger.error("Account registration is failed.")
            self.driver.close()
            assert False
        self.logger.info("**** test_001_AccountRegistration finished *** ")