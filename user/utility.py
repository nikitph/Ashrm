from flask import render_template
from flask.ext.mongoengine.wtf import model_form

__author__ = 'Omkareshwar'


def cruder(req, usr_model_class, template, route_name, display_name):
    mode = get_mode(req)
    # 1 = c, 2= r, 3=u, 4=d

    if mode == 1:
        usr_obj_form = model_form(usr_model_class)
        form = usr_obj_form(req.form)
        return render_template(template, form=form, mode=1, routename=route_name, displayname=display_name)

    elif mode == 2:
        mod_obj = usr_model_class.objects(id=req.args.get('id')).first()
        usr_obj_form = model_form(usr_model_class)
        form = usr_obj_form(req.form, mod_obj)
        return render_template(template, form=form, mode=2, routename=route_name, displayname=display_name)

    elif mode == 3:
        mod_obj = usr_model_class.objects(id=req.args.get('id')).first()
        usr_obj_form = model_form(usr_model_class)
        form = usr_obj_form(req.form, mod_obj)
        return render_template(template, form=form, mode=3, routename=route_name, displayname=display_name)

    elif mode == 4:
        mod_obj = usr_model_class.objects(id=req.args.get('id')).first()
        mod_obj.delete()
        return render_template(template, mode=4, routename=route_name, displayname=display_name)

    else:
        usr_obj_form = model_form(usr_model_class)
        form = usr_obj_form(req.form)
        return render_template(template, form=form, mode=1, routename=route_name, displayname=display_name)


def get_mode(req):
    mode = req.args.get('m')
    if mode == 'c':
        return 1
    elif mode == 'r':
        return 2
    elif mode == 'u':
        return 3
    elif mode == 'd':
        return 4