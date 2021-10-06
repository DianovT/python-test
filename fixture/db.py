import pymysql.cursors
from model.group import Group
from model.contact import Contact
from model.contact_in_group import Contact_in_Group


class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, database=name, user=user, password=password, autocommit=True)

    def get_group_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select group_id, group_name, group_header, group_footer from group_list")
            for row in cursor:
                (id, name, header, footer) = row
                list.append(Group(id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return list

    def get_contact_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, firstname, lastname, email, address ,home, mobile, work, email2, email3,"
                           " phone2 from addressbook where deprecated='0000-00-00 00:00:00'")
            for row in cursor:
                (id, firstname, lastname, EMail, address, home_phone, mob_phone, work_phone, EMail2, EMail3,
                 phone2) = row
                list.append(Contact(id=str(id), firstname=firstname, lastname=lastname, EMail=EMail, address=address,
                                    home_phone=home_phone, mob_phone=mob_phone, work_phone=work_phone,
                                    EMail2=EMail2, EMail3=EMail3, second_phone=phone2))
        finally:
            cursor.close()
        return list

    def get_contact_in_group_list(self):
        list_contact = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, group_id from address_in_groups where deprecated is Null")
            for row in cursor:
                (id_contact, id_group) = row
                list_contact.append(Contact_in_Group(id=str(id_contact), group_id=str(id_group)))
        finally:
            cursor.close()
        return list_contact

    def destroy(self):
        self.connection.close()