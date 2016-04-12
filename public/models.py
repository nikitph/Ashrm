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
    sections = db.IntField(required=True, verbose_name='Number of Sections')
    school = db.StringField(required=True, max_length=50, help_text='')

    def __str__(self):
        return self.standard

    __rpr__ = __str__


class Student(db.Document):
    school = db.StringField(required=True, max_length=20, help_text='')
    student_name = db.StringField(required=True, max_length=20, help_text='perm_identity')
    standard = db.ReferenceField(Standard, required=True, help_text='activateSlave(this);')
    section = db.StringField(required=True, max_length=5, verbose_name='Student Section',
                             help_text='airline_seat_legroom_extra')
    street_address = db.StringField(required=True, help_text='location_on')
    city = db.StringField(required=True, max_length=20, help_text='location_city')
    state = db.StringField(required=True, max_length=20, help_text='navigation')
    pincode = db.StringField(required=True, max_length=20, help_text='local_parking')
    phone = db.StringField(required=True, max_length=20, help_text='phone')
    email = db.StringField(required=True, max_length=20, help_text='email')
    date_of_birth = db.StringField(required=True, max_length=20, help_text='today')
    related = db.DictField(required=False)
    image = db.StringField(required=False, max_length=200,
                           default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')

    def __str__(self):
        return self.student_name

    __rpr__ = __str__


class Parent(db.Document):
    relationship = db.StringField(required=True, max_length=20, help_text='supervisor_account')
    parent_name = db.StringField(required=True, max_length=20, help_text='perm_identity')
    student_id = db.StringField(required=True, max_length=50, help_text='')
    street_address = db.StringField(required=True, help_text='location_on')
    city = db.StringField(required=True, max_length=20, help_text='location_city')
    state = db.StringField(required=True, max_length=20, help_text='navigation')
    pincode = db.StringField(required=True, max_length=20, help_text='local_parking')
    annual_income = db.StringField(required=True, max_length=50, help_text='monetization_on')
    occupation = db.StringField(required=True, max_length=50, help_text='work')
    phone = db.StringField(required=True, max_length=20, help_text='phone')
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
    code = db.StringField(required=True, max_length=50, help_text='code')
    subject_name = db.StringField(required=True, max_length=50, help_text='book')
    books = db.StringField(required=True, max_length=50, help_text='library_books')
    syllabus = db.StringField(required=True, max_length=50, help_text='content_paste')
    total_theory_hours = db.IntField(required=True, help_text='hourglass_empty')
    class_duration = db.IntField(required=True, help_text='hourglass_full')
    description = db.StringField(required=True, help_text='description')
    school = db.StringField(required=True, max_length=50, help_text='')

    def __str__(self):
        return self.subject_name

    __rpr__ = __str__


class Teacher(db.Document):
    teacher_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
    gender = db.BooleanField(required=True)
    street_address = db.StringField(required=True, help_text='location_on')
    city = db.StringField(required=True, max_length=20, help_text='location_city')
    state = db.StringField(required=True, max_length=20, help_text='navigation')
    pincode = db.StringField(required=True, max_length=20, help_text='local_parking')
    email = db.StringField(required=True, max_length=50, help_text='email')
    phone = db.StringField(required=True, max_length=50, help_text='phone')
    school = db.StringField(required=True, max_length=100, help_text='')

    def __str__(self):
        return self.teacher_name

    __rpr__ = __str__


class Profile(db.Document):
    user = db.StringField(required=True, max_length=50, help_text='')
    phone = db.StringField(required=True, max_length=50, help_text='phone')
    address = db.StringField(required=True, max_length=50, help_text='location_on')
    email = db.StringField(required=True, max_length=50, help_text='email')
    photo = db.StringField(required=True, max_length=50, help_text='')


class Event(db.Document):
    school = db.StringField(required=True, max_length=50, help_text='')
    event_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
    from_date = db.StringField(required=True, max_length=50, help_text='date_range')
    to_date = db.StringField(required=True, max_length=50, help_text='date_range')
    start_time = db.StringField(required=True, max_length=50, help_text='hourglass_full')
    end_time = db.StringField(required=True, max_length=50, help_text='hourglass_empty')
    location = db.StringField(required=True, max_length=50, help_text='location_on')
    event_for = db.StringField(required=True, verbose_name='Event is for',
                               choices=(('1', "Everyone"), ('2', "Students"), ('3', "Faculty"), ('4', "Parents")))
    description = db.StringField(required=True, help_text='description')


class BulkNotification(db.Document):
    school = db.StringField(required=True, max_length=50, help_text='')
    subject = db.StringField(required=True, max_length=200, help_text='mail_outline')
    body = db.StringField(required=True, verbose_name='Notification Message', help_text='subject')


class Conveyance(db.Document):
    school = db.StringField(required=True, max_length=50)
    registration_number = db.StringField(required=True, max_length=50, help_text='confirmation_number')
    total_seats = db.StringField(required=True, max_length=5, help_text='event_seat')
    maximum_capacity = db.StringField(required=True, max_length=50, help_text='arrow_upward')
    person_for_contact = db.StringField(required=True, max_length=50, help_text='perm_identity')
    contact_phone = db.StringField(required=True, max_length=50, help_text='phone')
    other_details = db.StringField(required=True, help_text='description')

    def __str__(self):
        return self.registration_number

    __rpr__ = __str__


class Driver(db.Document):
    school = db.StringField(required=True, max_length=50)
    driver_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
    street_address = db.StringField(required=True, help_text='location_on')
    city = db.StringField(required=True, max_length=20, help_text='location_city')
    state = db.StringField(required=True, max_length=20, help_text='navigation')
    pincode = db.StringField(required=True, max_length=20, help_text='local_parking')
    date_of_birth = db.StringField(required=True, max_length=20, help_text='today')
    contact_phone = db.StringField(required=True, max_length=50, help_text='phone')
    license_number = db.StringField(required=True, max_length=50, help_text='vpn_key')
    other_details = db.StringField(required=True, help_text='description')
    image = db.StringField(required=False, max_length=200,
                           default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')

    def __str__(self):
        return self.driver_name

    __rpr__ = __str__


class BusStop(db.Document):
    school = db.StringField(required=True, max_length=50)
    stop_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
    stop_address = db.StringField(required=True, help_text='location_on')
    landmark = db.StringField(required=True, max_length=150, help_text='navigation')
    pick_up_time = db.StringField(required=True, max_length=50, help_text='hourglass_full')

    def __str__(self):
        return self.stop_name

    __rpr__ = __str__


class BusRoute(db.Document):
    school = db.StringField(required=True, max_length=50)
    route_name = db.StringField(required=True, max_length=50, help_text='perm_identity')
    driver = db.ReferenceField(Driver, required=True)
    vehicle = db.ReferenceField(Conveyance, required=True)
    stops = db.ListField(ReferenceField(BusStop, required=True))

