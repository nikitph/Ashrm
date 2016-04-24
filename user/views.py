import datetime

from extensions import socketio
from flask import Blueprint, request, redirect, url_for, g, jsonify

from flask.ext.security import login_required, current_user, roles_required
from flask.ext.security.script import CreateUserCommand, AddRoleCommand
from flask.ext.socketio import emit
from flask.ext.sse import sse
from flask.templating import render_template
from werkzeug.utils import secure_filename
import wtforms
from flask.ext.mongoengine.wtf import model_form
from tasks import email

from public.models import *
from user.models import User, Role, Notification
from user.utility import cruder

bp_user = Blueprint('users', __name__, static_folder='../static')


@bp_user.before_request
def before_request():
    g.user = current_user


@bp_user.route('/')
def index():
    return render_template('index.html')


@bp_user.route('/send')
def send_message():
    sse.publish({"subject": '1', "id": '2'}, type='greeting')
    return "Message sent!"


@login_required
@bp_user.route('/setupd', methods=['GET'])
def setupd():
    iid = School.objects(id=g.user.schoolid).only('institute').first()
    return render_template('setupd.html', iid=str(iid.institute))


@login_required
@roles_required('admin')
@bp_user.route('/institute', methods=['GET', 'POST'])
def institute():
    if request.method == 'GET':
        a = Role.objects.filter(name='student').first()
        if a is None:
            Role(name='student').save()
        a = Role.objects.filter(name='parent').first()
        if a is None:
            Role(name='parent').save()
        a = Role.objects.filter(name='teacher').first()
        if a is None:
            Role(name='teacher').save()
        return cruder(request, Institute, 'institute.html', 'institute', 'Institute')

    else:
        obj_form = model_form(Institute)
        form = obj_form(request.form)
        if request.args['s'] == 't':
            return redirect(url_for('.school', m='c', s='t', iid=str(form.save().id)))
        return redirect(url_for('.institute', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/school', methods=['GET', 'POST'])
def school():
    if request.method == 'GET':
        # fields to be hidden come here
        field_args = {'user': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, School, 'school.html', 'school', 'School', field_args)

    else:
        obj_form = model_form(School)
        form = obj_form(request.form)
        sid = form.save().id
        User.objects(id=g.user.get_id()).update_one(set__school=request.form['school_name'])
        User.objects(id=g.user.get_id()).update_one(set__schoolid=str(sid))
        g.user.reload()
        if request.args['s'] == 't':
            return render_template('complete.html')
        return redirect(url_for('.school', m='r', id=str(sid)))


@login_required
@bp_user.route('/standard', methods=['GET', 'POST'])
def standard():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Standard, 'standard.html', 'standard', 'Standard', field_args, list_args,
                      g.user.schoolid)

    else:
        obj_form = model_form(Standard)
        form = obj_form(request.form)
        return redirect(url_for('.standard', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'GET':
        field_args = {'related': {'widget': wtforms.widgets.HiddenInput()},
                      'image': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'street_address': {'widget': wtforms.widgets.HiddenInput()},
                     'school': {'widget': wtforms.widgets.HiddenInput()},
                     'standard': {'widget': wtforms.widgets.HiddenInput()},
                     'image': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Student, 'student.html', 'student', 'Student', field_args, list_args
                      )

    else:
        obj_form = model_form(Student)
        form = obj_form(request.form)
        return redirect(url_for('.student', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/parent', methods=['GET', 'POST'])
def parent():
    if request.method == 'GET':
        field_args = {'student_id': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Parent, 'parent.html', 'parent', 'Parent', field_args)

    else:
        obj_form = model_form(Parent)
        form = obj_form(request.form)
        return redirect(url_for('.parent', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/scholarship', methods=['GET', 'POST'])
def scholarship():
    if request.method == 'GET':
        field_args = {'student_id': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Scholarship, 'scholarship.html', 'scholarship', 'Scholarship', field_args)

    else:
        obj_form = model_form(Scholarship)
        form = obj_form(request.form)
        return redirect(url_for('.scholarship', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/award', methods=['GET', 'POST'])
def award():
    if request.method == 'GET':
        field_args = {'student_id': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Award, 'award.html', 'award', 'Award', field_args)

    else:
        obj_form = model_form(Award)
        form = obj_form(request.form)
        return redirect(url_for('.award', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/transportation', methods=['GET', 'POST'])
def transportation():
    if request.method == 'GET':
        field_args = {'student_id': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'student_id': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Transportation, 'transportation.html', 'transportation',
                      'Transportation', field_args,
                      list_args, request.args['sid'])

    else:
        obj_form = model_form(Transportation)
        form = obj_form(request.form)
        return redirect(url_for('.transportation', m='r', id=str(form.save().id), sid=request.args['sid']))


@login_required
@bp_user.route('/hostelassignment', methods=['GET', 'POST'])
def hostelassignment():
    if request.method == 'GET':
        field_args = {'student_id': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'student_id': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, HostelAssignment, 'hostelassignment.html', 'hostelassignment',
                      'Hostel Assignment', field_args,
                      list_args, request.args['sid'])

    else:
        obj_form = model_form(HostelAssignment)
        form = obj_form(request.form)
        return redirect(url_for('.hostelassignment', m='r', id=str(form.save().id), sid=request.args['sid']))


@login_required
@bp_user.route('/subject', methods=['GET', 'POST'])
def subject():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Subject, 'subject.html', 'subject', 'Subject', field_args, list_args, g.user.schoolid)

    else:
        obj_form = model_form(Subject)
        form = obj_form(request.form)
        return redirect(url_for('.subject', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()},
                     'subjects': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Teacher, 'teacher.html', 'teacher', 'Teacher', field_args, list_args)

    else:
        obj_form = model_form(Teacher)
        form = obj_form(request.form)
        CreateUserCommand().run(email=request.form['email'], password='234765', active=1)
        AddRoleCommand().run(user_identifier=request.form['email'], role_name='teacher')
        return redirect(url_for('.teacher', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.datetime.now()
            filename = secure_filename(file.filename)
            file.save('static/img/' + filename)
            return jsonify({"filepath": 'static/img/' + filename})


@login_required
@bp_user.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@login_required
@bp_user.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')

    else:
        User.objects(id=g.user.get_id()).update_one(set__phone=request.form['phone'])
        User.objects(id=g.user.get_id()).update_one(set__address=request.form['address'])
        User.objects(id=g.user.get_id()).update_one(set__image=request.form['image'])
    return redirect(url_for('.student', m='l'))


@login_required
@bp_user.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}, 'event_for': {'radio': True}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        print(g.user.schoolid)
        return cruder(request, Event, 'event.html', 'event', 'Event', field_args, list_args, g.user.schoolid)

    else:
        obj_form = model_form(Event)
        form = obj_form(request.form)
        return redirect(url_for('.event', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/conveyance', methods=['GET', 'POST'])
def conveyance():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Conveyance, 'conveyance.html', 'conveyance', 'Conveyance', field_args, list_args,
                      g.user.schoolid)

    else:
        obj_form = model_form(Conveyance)
        form = obj_form(request.form)
        return redirect(url_for('.conveyance', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/driver', methods=['GET', 'POST'])
def driver():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()},
                      'image': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()},
                     'image': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Driver, 'driver.html', 'driver', 'Driver', field_args, list_args, g.user.schoolid)

    else:
        obj_form = model_form(Driver)
        form = obj_form(request.form)
        return redirect(url_for('.driver', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/busstop', methods=['GET', 'POST'])
def busstop():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, BusStop, 'busstop.html', 'busstop', 'Bus Stop', field_args, list_args,
                      g.user.schoolid)

    else:
        obj_form = model_form(BusStop)
        form = obj_form(request.form)
        return redirect(url_for('.busstop', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/busroute', methods=['GET', 'POST'])
def busroute():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, BusRoute, 'busroute.html', 'busroute', 'Bus Route', field_args, list_args,
                      g.user.schoolid)

    else:
        obj_form = model_form(BusRoute)
        form = obj_form(request.form)
        return redirect(url_for('.busroute', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/transportd', methods=['GET'])
def transportd():
    vehicle = Conveyance.objects().to_json()
    driver = Driver.objects().to_json()
    stop = BusStop.objects().to_json()
    route = BusRoute.objects().to_json()
    return render_template('transportd.html', vehicle=vehicle, driver=driver, stop=stop, route=route)


@login_required
@bp_user.route('/bulknotify', methods=['GET', 'POST'])
def bulknotify():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, BulkNotification, 'bulknotify.html', 'bulknotify', 'Bulk Notification', field_args,
                      list_args, g.user.schoolid)

    else:
        obj_form = model_form(BulkNotification)
        form = obj_form(request.form)
        id = str(form.save().id)
        x = Student.objects.only('email')
        rcp = []
        response = {"subject": form['subject'].data, "id" : id}
        socketio.emit('notification', response,namespace='/test')
        notif = Notification(subject=form['subject'].data, url=id)
        User.objects(id=g.user.get_id()).update_one(add_to_set__notif=notif)
        g.user.reload()


        for s in x:
            rcp.append(str(s.email))

        task = email.apply_async(args=[form['subject'].data, form['body'].data, rcp])
        return redirect(url_for('.bulknotify', m='r', id=id))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ['jpg', 'jpeg']


@login_required
@bp_user.route('/hosteld', methods=['GET'])
def hosteld():
    hostels = Hostel.objects().to_json()
    room = HostelRoom.objects().to_json()
    return render_template('hosteld.html', hostel=hostels, room=room)


@login_required
@bp_user.route('/hostel', methods=['GET', 'POST'])
def hostel():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Hostel, 'hostel.html', 'hostel', 'Hostel', field_args, list_args,
                      g.user.schoolid)

    else:
        obj_form = model_form(Hostel)
        form = obj_form(request.form)
        return redirect(url_for('.hostel', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/hostelroom', methods=['GET', 'POST'])
def hostelroom():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, HostelRoom, 'hostelroom.html', 'hostelroom', 'Hostel Room', field_args, list_args,
                      g.user.schoolid)

    else:
        obj_form = model_form(HostelRoom)
        form = obj_form(request.form)
        return redirect(url_for('.hostelroom', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/classroom', methods=['GET', 'POST'])
def classroom():
    if request.method == 'GET':
        field_args = {'school': {'widget': wtforms.widgets.HiddenInput()}}
        list_args = {'school': {'widget': wtforms.widgets.HiddenInput()},
                     'subjects': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, ClassRoom, 'classroom.html', 'classroom', 'Class Room', field_args, list_args,
                      g.user.schoolid)

    else:
        obj_form = model_form(ClassRoom)
        form = obj_form(request.form)
        return redirect(url_for('.classroom', m='r', id=str(form.save().id)))


@bp_user.route('/status/<task_id>')
def taskstatus(task_id):
    task = email.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


@socketio.on('join', namespace='/test')
def test_message(msg):
    response = {"subject": 'a', "id": 'b'}
    emit('notification', response)
