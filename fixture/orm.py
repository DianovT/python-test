from pony.orm import *
from datetime import datetime
from model.group import Group
from model.contact import Contact
from model.contact_in_group import Contact_in_Group

class ORMfixture:

    db = Database()

    class ORMGroup(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')
        contact_id = Set(lambda: ORMfixture.ORMContact, table="address_in_groups", column="id", reverse="group_id",
                       lazy=True)

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        firstname = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        deprecated = Optional(datetime, column='deprecated')
        group_id = Set(lambda: ORMfixture.ORMGroup, table="address_in_groups", column="group_id", reverse="contact_id",
                     lazy=True)

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_groups_to_model(self, groups):
        def convert(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))

    @db_session
    def get_group_list(self):
        return self.convert_groups_to_model(select(g for g in ORMfixture.ORMGroup))

    def convert_contact_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), firstname=contact.firstname, lastname=contact.lastname)
        return list(map(convert, contacts))

    @db_session
    def get_contact_list(self):
        return self.convert_contact_to_model(select(c for c in ORMfixture.ORMContact if c.deprecated is None))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORMfixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(orm_group.contact_id)

    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORMfixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(select(c for c in ORMfixture.ORMContact if c.deprecated is None
                                                     and orm_group not in c.group_id))
    @db_session
    def get_groups_with_contacts(self):
        list_groups = []
        group = self.db.select("group_id from address_in_groups")
        for i in group:
            list_groups.append(Contact_in_Group(id=str(i)))
        return list_groups

    def convert_contacts_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), firstname=contact.firstname, lastname=contact.lastname)
        return list(map(convert, contacts))