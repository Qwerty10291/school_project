from flask import Blueprint, render_template, abort, request, redirect
import db_additions
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user
import utils
from auth_forms import *

blueprint = Blueprint('auth', __name__)

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()

    if form.validate_on_submit():
        auth = db_additions.get_auth_data(request.form.get('login'))
        if not auth:
            return render_template('login.html', title='Вход', form=form, errors='Неправильный логин или пароль.')

        if not check_password_hash(auth.password, request.form.get('password')):
            return render_template('login.html', title='Вход', form=form, errors='Неправильный логин или пароль.')

        user = db_additions.get_user(auth.id)
        if not user.is_approved:
            return render_template('login.html', title='Вход', form=form, errors='Администратор не подтвердил заявку на регистрацию')

        login_user(db_additions.get_user(auth.id))
        return redirect('/')
    return render_template('login.html', title='Вход', form=form)


@blueprint.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form.get('username')
        login = request.form.get('login')

        if db_additions.check_login(login):
            return render_template('register.html', title='Регистрация', form=form, errors="Данный логин занят.")
        hashed_password = generate_password_hash(request.form.get('password'))

        if not utils.check_email(request.form['email']):
            return render_template('register.html', title='Регистрация', form=form, errors="Неправильный формат почты.")
        email = request.form.get('email')
        if db_additions.check_mail(email):
            return render_template('register.html', title='Регистрация', form=form, errors='Данная почта уже используется.')
        user = db_additions.register_user(login, hashed_password, email, name)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@blueprint.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/login')