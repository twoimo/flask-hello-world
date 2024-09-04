from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app.models.user import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            print("로그인 성공!!")
            return redirect(url_for('inquiry.inquiry_board'))
        print("로그인 실패!!")
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        # email = request.form.get('email')
        password = request.form.get('password')
        # address = request.form.get('address')
        
        user_instance = User.query.filter_by(username=username).first()
        # email_instance = User.query.filter_by(email=email).first()
        
        if user_instance:
            flash('이미 존재하는 사용자 이름입니다.')
            return redirect(url_for('auth.register'))
        
        # if email_instance:
        #     flash('이미 존재하는 이메일입니다.')
        #     return redirect(url_for('auth.register'))
        
        # new_user = User(username=username, email=email, address=address)
        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('회원가입이 완료되었습니다. 로그인 해주세요.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃 되었습니다.')
    return redirect(url_for('main.index'))