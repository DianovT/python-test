# -*- coding: utf-8 -*-
from model.contact import Сontact


    
def test_add_contact(app):
    old_contacts = app.contact.get_contact_list()
    contacts = Сontact(
            firstname="name1",
            middlename="name2",
            lastname="name3",
            nickname="testname",
            company="company",
            address="address",
            home_phone="9377722",
            mob_phone="23455552525",
            work_phone="2131231",
            second_phone="343434",
            EMail="test@test,com",
            bday="4",
            bmonth="March",
            byear="1988")
    app.contact.fill_new_form(contacts)
    assert len(old_contacts) + 1  == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts.append(contacts)
    assert sorted(old_contacts, key=Сontact.id_or_max) == sorted(new_contacts, key=Сontact.id_or_max)

