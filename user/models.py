from extensions import db
from flask.ext.security import UserMixin, RoleMixin
import datetime
from public.models import School


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80,unique=True)
    description = db.StringField(max_length=255)

    def __unicode__(self):
        return '%s' % self.name


class User(UserMixin, db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    email = db.StringField(max_length=255, required=True)
    username = db.StringField(max_length=255, required=False)
    password = db.StringField(required=True)
    active = db.BooleanField(default=False)
    first_name = db.StringField()
    last_name = db.StringField()
    image = db.StringField(required=False, max_length=200, default='static/img/256px-Weiser_State_Forest_Walking_Path.jpg')
    phone = db.StringField()
    school = db.StringField(max_length=255, required=False, default='')
    roles = db.ListField(db.ReferenceField(Role),default=[])
    #email confirmation
    confirmed_at = db.DateTimeField()
    #tracking
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField()
    current_login_ip = db.StringField()
    login_count = db.IntField()

    def __unicode__(self):
        return '%s' % self.id

    def __repr__(self):
        return "%s %s %s" % (self.username, self.id, self.email)


    def get_id(self):
        return unicode(self.id)

    def get_school(self):
        return unicode(self.school)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email', 'username'],
        'ordering': ['-created_at']
    }



