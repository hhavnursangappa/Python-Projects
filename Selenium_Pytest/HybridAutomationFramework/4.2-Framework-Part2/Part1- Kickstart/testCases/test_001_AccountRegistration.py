from pageObjects.HomePage import HomePage
from pageObjects.AccountRegistrationPage import AccountRegistrationPage

class Test_001_AccountReg:
    baseURL = "https://demo.opencart.com/"

    def test_account_reg(self,setup):
        self.driver = setup
        self.driver.get(self.baseURL)
        self.driver.maximize_window()

        self.hp=HomePage(self.driver)
        self.hp.clickMyAccount()
        self.hp.clickRegister()
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
        self.driver.close()
        if self.confmsg=="Your Account Has Been Created!":
            assert True
        else:
            assert False






