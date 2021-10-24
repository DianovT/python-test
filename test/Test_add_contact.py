# -*- coding: utf-8 -*-
from model.contact import Contact
import allure

def test_add_contact(app, db, check_ui, json_contacts):
    contact = json_contacts
    with allure.step('Given a contact list'):
        old_contacts = db.get_contact_list()
    with allure.step('When I add a contact %s to the list' % contact):
        app.contact.fill_new_form(contact)
    with allure.step('Then the new contact list is equal to the old list with the added contact'):
        assert len(old_contacts) + 1 == app.contact.count()
        new_contacts = db.get_contact_list()
        old_contacts.append(contact)
        assert old_contacts == new_contacts
        if check_ui:
            assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(), key=Contact.id_or_max)

