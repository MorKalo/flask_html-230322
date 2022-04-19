from flask import Flask, redirect, render_template, request, url_for, session, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from DB.User import  User
from DB.DbRepo import DbRepo
from DB.db_config import  local_session

repo = DbRepo(local_session)

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'Mor Kalo Moshe'


@app.route("/")
def home():
    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if 'remember' in session: #check if we remmber the user
            return redirect(url_for('my_app'))
        return render_template('signup.html') #else return to signup page
    form_data = request.form #return details from request
    username = form_data.get('username')
    print(username)
    email = form_data.get('email')
    print(email)
    password = form_data.get('password')
    print(password)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeated_password = request.form['repeated_password']
        if password != repeated_password:  # if passwords do not match
            return render_template('signup.html', bad_repeat=True)
        user=repo.get_user_by_email(email)
        if user:   # checking if username already exists
            return make_response('User alredy exists', 202)
        else:
            password = generate_password_hash(password_, method='sha256')
            new_user = User(public_id=str(uuid.uuid4()), username=username, password=hashed_password)
            repo.post_user(new_user)
            return render_template('my_app.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'remember' in session:  # the user want us to remember him?
            return redirect(url_for("my_app.html"))
        return render_template('login.html')
    if request.method == 'POST':
        form_data = request.form
        if not form_data.get('uname') or not form_data.get('psw'):         # check that no field is missing
            return make_response('some fields are missing', 401,
                                 {'WWW-Authenticate': 'Basic realm ="Login required!"'})
        user = repo.get_user_by_username(form_data.get('uname'))  # check if user exists in db
        if not user:
            return make_response('User does not exist', 401, {'WWW-Authenticate': 'Basic realm ="User does not exist"'})
        if not check_password_hash(user[0].password, form_data.get('psw')):  # check password
            return make_response('password did not match', 403, {'WWW-Authenticate': 'Basic realm ="Wrong Password"'})
        session['user'] = user[0].username
        if 'remember' in request.form:
            session['remember'] = True
        return render_template('my_app.html')

@app.route("/my_app")
def my_app():
    if 'user' in session:
        user = session['user']
        return render_template('my_app.html', user=user)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if 'user' in session:  # remove the user from the session
        session.pop('user')
    if 'remember' in session:  # remove remember from the session
        session.pop('remember')
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)