import configparser
import os

config = configparser.RawConfigParser()
config.read(os.path.abspath(os.curdir)+'\\HybridAutomationFramework\\OpenCartV1\\configurations\\config.ini')


class ReadConfig:
    @staticmethod
    def getApplicationURL():
        url = config.get(section='commonInfo', option='baseURL')
        return url

    @staticmethod
    def getUseremail():
        username = config.get(section='commonInfo', option='email')
        return username

    @staticmethod
    def getPassword():
        password = config.get(section='commonInfo', option='password')
        return password


#Testing above methods - optional Code
#print(ReadConfig.getApplicationURL())
#print(ReadConfig.getUseremail())
