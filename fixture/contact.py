from selenium.webdriver.support.ui import Select
from model.contact import Contact
import re



class ContactHelper:

    def __init__(self, app):
        self.app = app

    def open_home_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/addressbook") and len(wd.find_element_by_xpath("//input[@value='Delete']")) > 0):
            wd.find_element_by_link_text("home").click()

    def open_add_contact(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/edit.php") and len(wd.find_elements_by_name("submit")) > 0):
            wd.find_element_by_link_text("add new").click()

    def fill_new_form(self, contact):
        wd = self.app.wd
        self.open_add_contact()
        #fill_form
        self.fill_form(contact)
        #add_contact
        wd.find_element_by_xpath("//div[@id='content']/form/input[21]").click()
        self.contact_cache = None

    def fill_form(self, contact):
        wd = self.app.wd
        self.change_field_value("firstname", contact.firstname)
        self.change_field_value("middlename", contact.middlename)
        self.change_field_value("lastname", contact.lastname)
        self.change_field_value("nickname", contact.nickname)
        self.change_field_value("company", contact.company)
        self.change_field_value("address", contact.address)
        self.change_field_value("home", contact.home_phone)
        self.change_field_value("mobile", contact.mob_phone)
        self.change_field_value("work", contact.work_phone)
        self.change_field_value("phone2", contact.second_phone)
        self.change_field_value("email", contact.EMail)
        self.change_field_value("email2", contact.EMail2)
        self.change_field_value("email3", contact.EMail3)
        self.change_field_select("bday", contact.bday)
        self.change_field_select("bmonth", contact.bmonth)
        self.change_field_value("byear", contact.byear)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_field_select(self, field_select, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_select).click()
            Select(wd.find_element_by_name(field_select)).select_by_visible_text(text)

    def delete_first_contact(self):
        self.delete_contact_by_index(0)

    def delete_contact_by_index(self, index):
        wd = self.app.wd
        self.open_home_page()
        # select first contact
        self.select_contact_by_index(index)
        # submit deletion
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        wd.switch_to_alert().accept()
        self.contact_cache = None

    def modify_first_contact(self):
        self.modify_contact_by_index(0)

    def modify_contact_by_index(self, index, contact):
        wd = self.app.wd
        self.open_home_page()
        # edit first contact
        self.open_contact_edit_page_by_index(index)
        self.fill_form(contact)
        # accept edit
        wd.find_element_by_css_selector('input[value="Update"]').click()
        wd.find_element_by_link_text("home page").click()
        self.contact_cache = None

    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def open_contact_edit_page_by_index(self, index):
        wd = self.app.wd
        self.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def return_to_homepage(self):
        wd = self.app.wd
        wd.find_element_by_link_text("home page").click()

    def count(self):
        wd = self.app.wd
        self.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.open_home_page()
            self.contact_cache = []
            for row in wd.find_elements_by_name("entry"):
                cells = row.find_elements_by_tag_name("td")
                first_name = cells[2].text
                last_name = cells[1].text
                address = cells[3].text
                id = cells[0].find_element_by_name("selected[]").get_attribute("value")
                all_phone = cells[5].text
                all_EMail = cells[4].text
                self.contact_cache.append(Contact(lastname=last_name, firstname=first_name, address=address, id=id,
                                                  all_phones_from_homepage=all_phone, all_EMail_from_homepage = all_EMail))
        return list(self.contact_cache)

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_contact_edit_page_by_index(index)
        firstname = wd.find_element_by_name('firstname').get_attribute("value")
        lastname = wd.find_element_by_name('lastname').get_attribute("value")
        middlename = wd.find_element_by_name('middlename').get_attribute("value")
        address = wd.find_element_by_name('address').get_attribute("value")
        email = wd.find_element_by_name('email').get_attribute("value")
        email2 = wd.find_element_by_name('email2').get_attribute("value")
        email3 = wd.find_element_by_name('email3').get_attribute("value")
        id = wd.find_element_by_name('id').get_attribute("value")
        homephone = wd.find_element_by_name('home').get_attribute("value")
        mobilephone = wd.find_element_by_name('mobile').get_attribute("value")
        workphone = wd.find_element_by_name('work').get_attribute("value")
        secondaryphone = wd.find_element_by_name('phone2').get_attribute("value")
        return Contact(firstname=firstname,
                       lastname = lastname,
                       middlename=middlename,
                       address=address,
                       EMail=email,
                       EMail2=email2,
                       EMail3=email3,
                       id=id,
                       home_phone=homephone,
                       mob_phone=mobilephone,
                       work_phone=workphone,
                       second_phone=secondaryphone)

    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.open_home_page()
        row = wd.find_elements_by_name("entry")[index]
        cell = row.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_view_by_index(index)
        text = wd.find_element_by_id("content").text
        homephone = re.search("H: (.*)", text).group(1)
        mobilephone = re.search("M: (.*)", text).group(1)
        workphone = re.search("W: (.*)", text).group(1)
        secondaryphone = re.search("P: (.*)", text).group(1)
        return Contact(home_phone=homephone,
                       mob_phone=mobilephone,
                       work_phone=workphone,
                       second_phone=secondaryphone)


    def delete_contact_by_id(self, id):
        wd = self.app.wd
        self.open_home_page()
        # select first contact
        self.select_contact_by_id(id)
        # submit deletion
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        wd.switch_to_alert().accept()
        wd.find_element_by_link_text("home").click()
        self.contact_cache = None

    def select_contact_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector("input[value='%s']" % id).click()


    def open_contact_edit_page_by_id(self, id):
        wd = self.app.wd
        self.open_home_page()
        wd.find_element_by_css_selector('a[href="edit.php?id=%s"]' % id).click()

    def modify_contact_by_id(self, id, contact):
        wd = self.app.wd
        self.open_home_page()
        # edit first contact
        self.open_contact_edit_page_by_id(id)
        self.fill_form(contact)
        # accept edit
        wd.find_element_by_css_selector('input[value="Update"]').click()
        wd.find_element_by_link_text("home page").click()
        self.contact_cache = None




