import datetime
import os

from flask import Flask, url_for, request, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.login import LoginForm

from flask_login import LoginManager, login_user

from flask_restful import reqparse, abort, Api, Resource
import users_resources, jobs_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/first')
def first():
    return 'просто какая-то страница'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def add_user():
    user = User()
    user.surname = 'Scott'
    user.name = 'Ridley'
    user.age = 16
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_1'
    user.email = 'scott_chief@mars.org'
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    user2 = User()
    user2.surname = 'Blake'
    user2.name = 'Franklin'
    user2.age = 19
    user2.position = 'manager'
    user2.speciality = 'police officer'
    user2.address = 'module_2'
    user2.email = 'blake_and_black@mars.org'
    db_sess = db_session.create_session()
    db_sess.add(user2)
    db_sess.commit()

    user3 = User()
    user3.surname = 'Ablewhite'
    user3.name = 'Godfrey'
    user3.age = 22
    user3.position = 'second captain'
    user3.speciality = 'scientist'
    user3.address = 'module_3'
    user3.email = 'godfrey_is_the_best@mars.org'
    db_sess = db_session.create_session()
    db_sess.add(user3)
    db_sess.commit()

    user4 = User()
    user4.surname = 'Spearman'
    user4.name = 'Rosanna'
    user4.age = 20
    user4.position = 'cleaner'
    user4.speciality = 'housemaid'
    user4.address = 'module_2'
    user4.email = 'spearman@mars.org'
    db_sess = db_session.create_session()
    db_sess.add(user4)
    db_sess.commit()


def add_job():
    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    db_sess = db_session.create_session()
    db_sess.add(job)
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init(f"db/mars_explorer.db")
    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)