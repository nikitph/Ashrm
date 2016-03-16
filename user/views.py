from flask import Blueprint, request, session, redirect, url_for, flash, g
from flask.ext.security import login_required, logout_user, login_user, current_user
from flask.templating import render_template
from public.models import Institute, School, Student, Standard
from flask.ext.mongoengine.wtf import model_form
from user.models import User
from user.utility import cruder

bp_user = Blueprint('users', __name__, static_folder='../static')


@bp_user.before_request
def before_request():
    g.user = current_user


@bp_user.route('/')
def index():
    return render_template('index.html')


@login_required
@bp_user.route('/institute', methods=['GET'])
def institute_get():
    return render_template('institute.html')


@login_required
@bp_user.route('/institute', methods=['POST'])
def institute_post():
    data = request.form
    print(data)
    nam = data['institute']
    addre = data['address']
    cit = data['city']
    sta = data['state']
    pin = data['pincode']
    p = data['phone']
    w = data['website']
    e = data['email']
    inst = Institute(name=nam, address=addre, city=cit, state=sta, pincode=pin, phone=p, website=w, email=e)
    print(inst.save())
    return redirect('/school/' + str(inst.id))


@login_required
@bp_user.route('/school/<iid>', methods=['GET'])
def school_get(iid):
    school_form = model_form(School)
    form = school_form(request.form)
    return render_template('school.html', institute=iid, form=form)


@login_required
@bp_user.route('/school', methods=['POST'])
def school_post():
    school_f = model_form(School)
    sc = school_f(request.form)
    t = sc.save()
    User.objects(id=g.user.get_id()).update_one(set__school=request.form['school_name'])
    g.user.reload()
    return redirect('/classes/' + str(t.id))


@login_required
@bp_user.route('/classes/<sid>', methods=['GET'])
def classes_get(sid):
    ft = model_form(Standard)
    f = ft(request.form)
    return render_template('classes.html', form=f, scid=sid)


@login_required
@bp_user.route('/classes', methods=['POST'])
def classes_post():
    classes_form = model_form(Standard)
    form = classes_form(request.form)
    form.save()
    return render_template('complete.html')


@login_required
@bp_user.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'GET':
        return cruder(request, Student, 'student.html', 'student', 'Student')

    else:
        obj_form = model_form(Student)
        form = obj_form(request.form)
        return redirect(url_for('.student', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/dashboard/', methods=['GET'])
def dashboard_get():
    return render_template('dashboard.html')
