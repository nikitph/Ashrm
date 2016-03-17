from mongoengine import EmbeddedDocumentField, ListField, Document, DynamicDocument, ReferenceField
from wtforms import FieldList, StringField
from extensions import db


class Institute(db.Document):
    name = db.StringField(required=True, max_length=50)
    address = db.StringField(required=True)
    city = db.StringField(required=True, max_length=50)
    state = db.StringField(required=True, max_length=50)
    pincode = db.IntField(required=True)
    phone = db.StringField(required=True, max_length=50)
    website = db.StringField(required=True, max_length=50)
    email = db.StringField(required=True, max_length=50)

    def __str__(self):
        return self.name

    __rpr__ = __str__


class School(db.Document):
    institute = db.ReferenceField(Institute, required=True)
    user = db.StringField(required=True, max_length=50)
    school_name = db.StringField(required=True, max_length=50)
    street_address = db.StringField(required=True)
    city = db.StringField(required=True, max_length=50)
    state = db.StringField(required=True, max_length=50)
    pincode = db.IntField(required=True)
    phone = db.StringField(required=True, max_length=50)
    website = db.StringField(required=True, max_length=50)
    email = db.StringField(required=True, max_length=50)


class Standard(db.Document):
    standard = db.StringField(required=True, max_length=20)
    sections = db.IntField(required=True)
    school = db.StringField(required=True, max_length=50)

    def __str__(self):
        return self.standard

    __rpr__ = __str__


class Student(db.Document):
    school = db.StringField(required=True, max_length=20)
    student_name = db.StringField(required=True, max_length=20)
    standard = db.ReferenceField(Standard, required=True)
    street_address = db.StringField(required=True)
    city = db.StringField(required=True, max_length=20)
    state = db.StringField(required=True, max_length=20)
    pincode = db.StringField(required=True, max_length=20)
    phone = db.StringField(required=True, max_length=20)
    email = db.StringField(required=True, max_length=20)
    related = db.DictField(required=False)

    def __str__(self):
        return self.student_name

    __rpr__ = __str__


class Parent(db.Document):
    relationship = db.StringField(required=True, max_length=20)
    parent_name = db.StringField(required=True, max_length=20)
    student_id = db.StringField(required=True, max_length=50)
    street_address = db.StringField(required=True)
    city = db.StringField(required=True, max_length=20)
    state = db.StringField(required=True, max_length=20)
    pincode = db.StringField(required=True, max_length=20)
    annual_income = db.StringField(required=True, max_length=50)
    occupation = db.StringField(required=True, max_length=50)
    phone = db.StringField(required=True, max_length=20)
    email = db.StringField(required=True, max_length=20)

    def save(self, *args, **kwargs):
        super(Parent, self).save(*args, **kwargs)
        stu = Student.objects(id=self.student_id).first()
        keys = {str(self.id): 'parent'}
        set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
        stu.update(**set_new)


class Scholarship(db.Document):
    awarding_body = db.StringField(required=True, max_length=20)
    year = db.StringField(required=True, max_length=20)
    student_id = db.StringField(required=True, max_length=50)
    title_of_scholarship = db.StringField(required=True)

    def save(self, *args, **kwargs):
        super(Scholarship, self).save(*args, **kwargs)
        stu = Student.objects(id=self.student_id).first()
        keys = {str(self.id): 'scholarship'}
        set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
        stu.update(**set_new)

