# -*- coding: utf-8 -*-

import flask_security
from flask_login import current_user
from flask import g, session, flash, redirect, request, render_template
from flask_security.utils import logout_user
from optparse import OptionParser
from user_portrait import create_app
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
            UserMixin, RoleMixin, login_required
from user_portrait.extensions import db, user_datastore

optparser = OptionParser()
optparser.add_option('-p', '--port', dest='port', help='Server Http Port Number', default=9001, type='int')
(options, args) = optparser.parse_args()

# Create app
app = create_app()

# Create user role data to test with
@app.route('/create_user_role_test')
def create_user_roles():
    try:
        db.create_all()
        role_1 = user_datastore.create_role(name='attribute', description='role for attribute module')
        role_2 = user_datastore.create_role(name='detect', description='role for detect module')
        role_3 = user_datastore.create_role(name='group', description='role for group module')
        role_4 = user_datastore.create_role(name='influence_application', description='role for influence_application')
        role_5 = user_datastore.create_role(name='manage', description='role for manage module')
        role_6 = user_datastore.create_role(name='overview', description='role for overview module')
        role_7 = user_datastore.create_role(name='profile', description='role for profile module')
        role_8 = user_datastore.create_role(name='recommentation', description='role for recommentation module')
        role_9 = user_datastore.create_role(name='social_sensing', description='role for social_sensing module')
        
        user_1 = user_datastore.create_user(email='linhao.lh@qq.com', password="Bh123456")
        user_2 = user_datastore.create_user(email='test@test.com', password="Bh123456")
        user_datastore.add_role_to_user(user_1, role_1)
        user_datastore.add_role_to_user(user_1, role_2)
        user_datastore.add_role_to_user(user_1, role_3)
        user_datastore.add_role_to_user(user_1, role_4)
        user_datastore.add_role_to_user(user_1, role_5)
        user_datastore.add_role_to_user(user_1, role_6)
        user_datastore.add_role_to_user(user_1, role_7)
        user_datastore.add_role_to_user(user_1, role_8)
        user_datastore.add_role_to_user(user_1, role_9)
        user_datastore.add_role_to_user(user_2, role_1)
        db.session.commit()
        return "success"
    except:
        db.session.rollback()
        return "failure"

@app.before_request
def before_request():
    g.user = current_user

@app.after_request
def after_request(response):
    return response

@app.route('/')
def homepage():
    return render_template('homepage.html')

# logout
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash(u'You have been signed out')

    return redirect("/login") #redirect(request.args.get('next', None))

# app run
app.run(host='0.0.0.0', port=options.port)
