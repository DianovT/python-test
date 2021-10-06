from selenium.webdriver.support.ui import Select


class Contact_in_Group_Helper:

    def __init__(self, cing):
        self.cing = cing

    def back_home_page(self):
        wd = self.cing.wd
        if not(wd.current_url.endswith("addressbook/") and len(wd.find_element_by_name("to_group")) > 0):
            wd.find_element_by_link_text("home").click()

    def count(self):
        wd = self.cing.wd
        self.cing.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    contact_cash = None

    def get_list_contact_in_group(self, group_id):
        wd = self.cing.wd
        wd.find_element_by_name("group").click()
        wd.find_element_by_xpath("//option[@value='%s']" % group_id).click()

    def select_contact(self, id_contact):
        wd = self.cing.wd
        wd.find_element_by_css_selector("input[id='%s']" % id_contact).click()

    def select_group(self, text, id_group):
        wd = self.cing.wd
        wd.find_element_by_css_selector("select[name='%s'" % text + "]>option[value='%s']" % id_group.id).click()

    def add_contact_in_group(self, id_contact, id_group):
        wd = self.cing.wd
        self.cing.open_home_page()
        Select(wd.find_element_by_name("group")).select_by_visible_text('[none]')
        self.select_contact(id_contact)
        self.select_group("to_group", id_group)
        wd.find_element_by_xpath("(//input[@value='Add to'])").click()
        self.back_home_page()
        self.contact_cash = None


    def del_contact_in_group_by_id(self, contact, group):
        wd = self.cing.wd
        self.cing.open_home_page()
        self.select_group("group", group)
        self.select_contact(contact)
        wd.find_element_by_name("remove")
        wd.find_element_by_name("remove").click()
        wd.find_element_by_css_selector("div.msgbox")
        wd.find_element_by_link_text("home").click()
        self.contact_cash = None