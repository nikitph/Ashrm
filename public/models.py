from mongoengine import EmbeddedDocumentField, ListField, Document, DynamicDocument
from wtforms import FieldList, StringField
from extensions import db
from flask.ext.mongoengine.wtf import model_form



class Institute(db.Document):
    name = db.StringField(required=True)
    address = db.StringField(required=True)
    city = db.StringField(required=False)
    state = db.StringField(required=True)
    country = db.StringField(required=False)
    pincode = db.IntField(required=True)
    phone = db.StringField(required=True)
    website = db.StringField(required=True)
    email = db.StringField(required=True)


class School(db.Document):
    institute = db.StringField(required=True, max_length=50)
    school_name = db.StringField(required=True, max_length=50)
    street_address = db.StringField(required=True)
    city = db.StringField(required=True, max_length=50)
    state = db.StringField(required=True, max_length=50)
    pincode = db.IntField(required=True)
    phone = db.StringField(required=True, max_length=50)
    website = db.StringField(required=True, max_length=50)
    email = db.StringField(required=True, max_length=50)


class Standard1(db.EmbeddedDocument):
    standard = db.StringField(required=True, max_length=20)
    sections = db.IntField(required=True)
    school = db.StringField(required=True, max_length=50)


class Student(db.Document):
    school = db.StringField(required=True, max_length=20)
    student_name = db.StringField(required=True, max_length=20)
    standard = db.StringField(required=True, max_length=20)
    street_address = db.StringField(required=True)
    city = db.StringField(required=True, max_length=20)
    state = db.StringField(required=True, max_length=20)
    pincode = db.StringField(required=True, max_length=20)
    phone = db.StringField(required=True, max_length=20)
    email = db.StringField(required=True, max_length=20)


class Standards(db.Document):
    Standrds = db.ListField(EmbeddedDocumentField(Standard1))
