from flask import Blueprint, request, session, redirect, url_for, flash, g
from flask.ext.security import login_required, logout_user, login_user, current_user
from flask.templating import render_template
import wtforms
from public.models import Institute, School, Student, Standard, Parent, Scholarship
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
@bp_user.route('/institute', methods=['GET', 'POST'])
def institute():
    if request.method == 'GET':
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
        field_args = {'user': {'widget': wtforms.widgets.HiddenInput()},
                      'city': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, School, 'school.html', 'school', 'School', field_args)

    else:
        obj_form = model_form(School)
        form = obj_form(request.form)
        sid = form.save().id
        User.objects(id=g.user.get_id()).update_one(set__school=request.form['school_name'])
        g.user.reload()
        if request.args['s'] == 't':
            return redirect(url_for('.standard', m='c', s='t', sid=str(sid)))
        return redirect(url_for('.school', m='r', id=str(sid)))


@login_required
@bp_user.route('/standard', methods=['GET', 'POST'])
def standard():
    if request.method == 'GET':
        return cruder(request, Standard, 'standard.html', 'standard', 'Standard')

    else:
        obj_form = model_form(Standard)
        form = obj_form(request.form)
        if request.args['s'] == 't':
            return redirect(url_for('.standard', m='c', id=str(form.save().id), sid=request.args['sid']))
        if request.args['s'] == 'c':
            return render_template('complete.html', id=str(form.save().id))
        return redirect(url_for('.standard', m='r', id=str(form.save().id)))


@login_required
@bp_user.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'GET':
        field_args = {'related': {'widget': wtforms.widgets.HiddenInput()}}
        return cruder(request, Student, 'student.html', 'student', 'Student', field_args)

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
@bp_user.route('/dashboard/', methods=['GET'])
def dashboard_get():
    return render_template('dashboard.html')
