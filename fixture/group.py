


class GroupHelper:

    def __init__(self, app):
        self.app = app

    def open_groups(self):
        wd = self.app.wd
        wd.find_element_by_link_text("groups").click()

    def create(self, Group):
        wd = self.app.wd
        self.open_groups()
        # init_groups_creation
        wd.find_element_by_name("new").click()
        #fill_group_form
        wd.find_element_by_name("group_name").click()
        wd.find_element_by_name("group_name").clear()
        wd.find_element_by_name("group_name").send_keys(Group.name)
        wd.find_element_by_name("group_header").click()
        wd.find_element_by_name("group_header").clear()
        wd.find_element_by_name("group_header").send_keys(Group.header)
        wd.find_element_by_name("group_footer").click()
        wd.find_element_by_name("group_footer").clear()
        wd.find_element_by_name("group_footer").send_keys(Group.footer)
        #submit_group_creation
        wd.find_element_by_name("submit").click()
        self.return_to_group_page()

    def return_to_group_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("group page").click()