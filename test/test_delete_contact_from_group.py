from model.group import Group
from model.contact import Contact
import random


def test_del_contact_in_group(app, db, orm):
    if len(db.get_contact_list()) == 0:
        app.contact.fill_new_form(Contact(firstname="firstname"))
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="name", header="header", footer="footer"))

    if len(db.get_contact_in_group_list()) == 0:
        list_group = db.get_group_list()
        choice_id_group = random.choice(list_group)
        contact_not_in_group = orm.get_contacts_not_in_group(choice_id_group)
        choice_id_contact = random.choice(contact_not_in_group)
        app.cing.add_contact_in_group(choice_id_contact.id, choice_id_group)

    old_list_contact_in_group = orm.get_groups_with_contacts()

    choice_id_group = random.choice(old_list_contact_in_group)
    contact_in_group = orm.get_contacts_in_group(choice_id_group)
    choice_id_contact = random.choice(contact_in_group)
    app.cing.del_contact_in_group_by_id(choice_id_contact.id, choice_id_group)
    new_list_contact_in_group = orm.get_contacts_in_group(choice_id_group)
    contact_in_group.remove(choice_id_contact)
    assert contact_in_group == new_list_contact_in_group