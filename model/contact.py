from sys import maxsize

class contact:
    def __init__(self, firstname=None, middlename=None, lastname=None, nickname=None, company=None, address=None, home_number=None,
                          mob_number=None, work_number=None, EMail=None, bday=None, bmonth=None, byear=None, id=None):
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.nickname = nickname
        self.company = company
        self.address = address
        self.home_number = home_number
        self.mob_number = mob_number
        self.work_number = work_number
        self.EMail = EMail
        self.bday = bday
        self.bmonth = bmonth
        self.byear = byear
        self.id = id

    def __repr__(self):
        return "%s:%s:%s" % (self.id, self.firstname, self.lastname)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) \
               and self.firstname == other.firstname \
               and self.lastname == other.lastname

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
