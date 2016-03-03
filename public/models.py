from extensions import db


class Institute(db.Document):
    name = db.StringField(required=True)
    street_address = db.StringField(required=True)
    city = db.StringField(required=False)
    state = db.StringField(required=True)
    country = db.StringField(required=False)
    pincode = db.IntField(required=True)
    phone = db.StringField(required=True)
    website = db.StringField(required=True)
    email = db.StringField(required=True)
    tin = db.StringField(required=True)


class School(db.Document):
    institute = db.StringField(required=True)
    name = db.StringField(required=True)
    street_address = db.StringField(required=True)
    city = db.StringField(required=False)
    state = db.StringField(required=True)
    country = db.StringField(required=False)
    pincode = db.IntField(required=True)
    phone = db.StringField(required=True)
    website = db.StringField(required=True)
    email = db.StringField(required=True)


class Standard(db.Document):
    standard_id = db.StringField(required=True)
    section = db.StringField(required=True)
    school = db.StringField(required=True)


class Student(db.Document):
    school = db.StringField(required=True)
    standard = db.StringField(required=True)
    name = db.StringField(required=True)
    street_address = db.StringField(required=True)
    city = db.StringField(required=False)
    state = db.StringField(required=True)
    country = db.StringField(required=False)
    pincode = db.IntField(required=True)
    phone = db.StringField(required=True)
    website = db.StringField(required=True)
    email = db.StringField(required=True)

