from model.group import Group
from model.contact import Contact
from model.contact_in_group import Contact_in_Group
import random


def test_add_contact_in_group(app, db, orm):
    if len(db.get_contact_list()) == 0:
        app.contact.fill_new_form(Contact(firstname="firstname"))
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="name", header="header", footer="footer"))
    old_list_contact_in_group = db.get_contact_in_group_list()
    list_group = db.get_group_list()
    choice_id_group = random.choice(list_group)
    if len(orm.get_contacts_not_in_group(choice_id_group)) == 0:
        app.contact.fill_new_form(Contact(lastname="lastname"))

    contact_not_in_group = orm.get_contacts_not_in_group(choice_id_group)
    choice_id_contact = random.choice(contact_not_in_group)

    app.cing.add_contact_in_group(choice_id_contact.id, choice_id_group)
    new_list_contact_in_group = db.get_contact_in_group_list()
    assert len(old_list_contact_in_group) + 1 == len(new_list_contact_in_group)
    old_list_contact_in_group.append(Contact_in_Group(id=choice_id_contact.id))
    assert sorted(old_list_contact_in_group, key=Contact_in_Group.id_max) == \
           sorted(new_list_contact_in_group, key=Contact_in_Group.id_max)
