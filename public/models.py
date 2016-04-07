from mongoengine import EmbeddedDocumentField, ListField, Document, DynamicDocument, ReferenceField
from wtforms import FieldList, StringField
from extensions import db


class Institute(db.Document):
    name = db.StringField(required=True, max_length=50, help_text='perm_identity')
    address = db.StringField(required=True, help_text='location_on')
    city = db.StringField(required=True, max_length=50, help_text='location_city')
    state = db.StringField(required=True, max_length=50, help_text='location_searching')
    pincode = db.IntField(required=True)
    phone = db.StringField(required=True, max_length=50, help_text='phone')
    website = db.StringField(required=True, max_length=50, help_text='web')
    email = db.StringField(required=True, max_length=50, help_text='email')

    def __str__(self):
        return self.name

    __rpr__ = __str__


class School(db.Document):
    institute = db.StringField(required=True, max_length=100, help_text='')
    user = db.StringField(required=True, max_length=50, help_text='')
    school_name = db.StringField(required=True, max_length=50, help_text='')
    street_address = db.StringField(required=True)
    city = db.StringField(required=True, max_length=50, help_text='')
    state = db.StringField(required=True, max_length=50, help_text='')
    pincode = db.IntField(required=True)
    phone = db.StringField(required=True, max_length=50, help_text='')
    website = db.StringField(required=True, max_length=50, help_text='')
    email = db.StringField(required=True, max_length=50, help_text='')


class Standard(db.Document):
    standard = db.StringField(required=True, max_length=20, help_text='')
    sections = db.IntField(required=True)
    school = db.StringField(required=True, max_length=50, help_text='')

    def __str__(self):
        return self.standard

    __rpr__ = __str__


class Student(db.Document):
    school = db.StringField(required=True, max_length=20, help_text='')
    student_name = db.StringField(required=True, max_length=20, help_text='')
    standard = db.ReferenceField(Standard, required=True)
    street_address = db.StringField(required=True)
    city = db.StringField(required=True, max_length=20, help_text='')
    state = db.StringField(required=True, max_length=20, help_text='')
    pincode = db.StringField(required=True, max_length=20, help_text='')
    phone = db.StringField(required=True, max_length=20, help_text='')
    email = db.StringField(required=True, max_length=20, help_text='')
    date_of_birth = db.StringField(required=True, max_length=20, help_text='')
    related = db.DictField(required=False)
    image = db.StringField(required=False, max_length=200,
                           default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')

    def __str__(self):
        return self.student_name

    __rpr__ = __str__


class Parent(db.Document):
    relationship = db.StringField(required=True, max_length=20, help_text='')
    parent_name = db.StringField(required=True, max_length=20, help_text='perm_identity')
    student_id = db.StringField(required=True, max_length=50, help_text='')
    street_address = db.StringField(required=True, help_text='location_on')
    city = db.StringField(required=True, max_length=20, help_text='')
    state = db.StringField(required=True, max_length=20, help_text='')
    pincode = db.StringField(required=True, max_length=20, help_text='')
    annual_income = db.StringField(required=True, max_length=50, help_text='')
    occupation = db.StringField(required=True, max_length=50, help_text='')
    phone = db.StringField(required=True, max_length=20, help_text='')
    email = db.StringField(required=True, max_length=20, help_text='email')

    def save(self, *args, **kwargs):
        super(Parent, self).save(*args, **kwargs)
        stu = Student.objects(id=self.student_id).first()
        keys = {str(self.id): 'parent'}
        set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
        stu.update(**set_new)


class Scholarship(db.Document):
    awarding_body = db.StringField(required=True, max_length=20, help_text='')
    year = db.StringField(required=True, max_length=20, help_text='')
    student_id = db.StringField(required=True, max_length=50, help_text='')
    title_of_scholarship = db.StringField(required=True)

    def save(self, *args, **kwargs):
        super(Scholarship, self).save(*args, **kwargs)
        stu = Student.objects(id=self.student_id).first()
        keys = {str(self.id): 'scholarship'}
        set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
        stu.update(**set_new)


class Award(db.Document):
    awarding_body = db.StringField(required=True, max_length=20, help_text='')
    year = db.StringField(required=True, max_length=20, help_text='')
    student_id = db.StringField(required=True, max_length=50, help_text='')
    title_of_award = db.StringField(required=True)

    def save(self, *args, **kwargs):
        super(Award, self).save(*args, **kwargs)
        stu = Student.objects(id=self.student_id).first()
        keys = {str(self.id): 'award'}
        set_new = dict((("set__related__%s" % k, v) for k, v in keys.iteritems()))
        stu.update(**set_new)


class Subject(db.Document):
    code = db.StringField(required=True, max_length=50, help_text='')
    subject_name = db.StringField(required=True, max_length=50, help_text='')
    books = db.StringField(required=True, max_length=50, help_text='')
    syllabus = db.StringField(required=True, max_length=50, help_text='')
    total_theory_hours = db.IntField(required=True)
    class_duration = db.IntField(required=True)
    description = db.StringField(required=True)
    school = db.StringField(required=True, max_length=50, help_text='')

    def __str__(self):
        return self.subject_name

    __rpr__ = __str__


class Teacher(db.Document):
    teacher_name = db.StringField(required=True, max_length=50, help_text='')
    gender = db.BooleanField(required=True)
    street_address = db.StringField(required=True)
    city = db.StringField(required=True, max_length=20, help_text='')
    state = db.StringField(required=True, max_length=20, help_text='')
    pincode = db.StringField(required=True, max_length=20, help_text='')
    school = db.StringField(required=True, max_length=100, help_text='')

    def __str__(self):
        return self.teacher_name

    __rpr__ = __str__


class Profile(db.Document):
    user = db.StringField(required=True, max_length=50, help_text='')
    phone = db.StringField(required=True, max_length=50, help_text='')
    address = db.StringField(required=True, max_length=50, help_text='')
    email = db.StringField(required=True, max_length=50, help_text='')
    photo = db.StringField(required=True, max_length=50, help_text='')


class Event(db.Document):
    school = db.StringField(required=True, max_length=50, help_text='')
    event_name = db.StringField(required=True, max_length=50, help_text='')
    from_date = db.StringField(required=True, max_length=50, help_text='')
    to_date = db.StringField(required=True, max_length=50, help_text='')
    start_time = db.StringField(required=True, max_length=50, help_text='')
    end_time = db.StringField(required=True, max_length=50, help_text='')
    location = db.StringField(required=True, max_length=50, help_text='')
    event_for = db.StringField(required=True, verbose_name='Event is for',
                               choices=(('1', "Everyone"), ('2', "Students"), ('3', "Faculty"), ('4', "Parents")))
    description = db.StringField(required=True)


class BulkNotification(db.Document):
    school = db.StringField(required=True, max_length=50, help_text='')
    subject = db.StringField(required=True, max_length=200, help_text='')
    body = db.StringField(required=True, verbose_name='Notification Message')
