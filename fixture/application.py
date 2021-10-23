from selenium import webdriver
from fixture.session import SessionHelper
from fixture.group import GroupHelper
from fixture.contact import ContactHelper
from fixture.contact_in_group import Contact_in_Group_Helper
from webdriver_manager.firefox import GeckoDriverManager


class Application:

    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox(executable_path="C:\Python\Python39\geckodriver.exe")
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "IE":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)
        self.contact = ContactHelper(self)
        self.cing = Contact_in_Group_Helper(self)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)
        return wd

    def destroy(self):
        self.wd.quit()
