from flask import  render_template, url_for, flash, redirect,request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user,logout_user, login_required


posts = [
    {
        'author': 'John Smith',
        'title': 'Introduction to Python',
        'content': 'Python is a versatile programming language...',
        'date_posted': '2023-05-01'
    },
    {
        'author': 'Jane Doe',
        'title': 'Data Analysis with Pandas',
        'content': 'Pandas is a powerful library for data manipulation...',
        'date_posted': '2023-05-05'
    },
    {
        'author': 'Mike Johnson',
        'title': 'Web Development with Django',
        'content': 'Django is a popular web framework for Python...',
        'date_posted': '2023-05-10'
    },
    {
        'author': 'Sarah Thompson',
        'title': 'Machine Learning Basics',
        'content': 'Machine learning is a branch of artificial intelligence...',
        'date_posted': '2023-05-15'
    },
    {
        'author': 'David Williams',
        'title': 'JavaScript Fundamentals',
        'content': 'JavaScript is a scripting language used for web development...',
        'date_posted': '2023-05-20'
    },
    {
        'author': 'Emily Wilson',
        'title': 'Introduction to Data Science',
        'content': 'Data science involves extracting insights from data...',
        'date_posted': '2023-05-25'
    },
    {
        'author': 'Mark Anderson',
        'title': 'Artificial Intelligence Applications',
        'content': 'AI is revolutionizing various industries...',
        'date_posted': '2023-05-30'
    }
]

@app.route('/')
def home():
    return render_template('home.html',posts=posts,title= 'Home')

@app.route('/about')
def about():
    return  render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password )
        db.session.add(user)
        db.session.commit()
        flash(f'ანგარიში წარმატებით შეიქმნა {form.username.data}-ისთვის!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration Form', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('წვდომა წარუმატებელია.გთხოვთ გადაამოწმოთ მეილი და პაროლი','danger')
    return  render_template('login.html', title='Login Page',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'ანგარიში წარმატებით განახლდა {form.username.data}-სთვის!','success')
        return  redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return  render_template('account.html', title='Account', image_file=image_file , form=form)
