from flask_app import app, render_template, redirect, request, session, flash
from flask_app import bcrypt
from flask_app.models.user import User

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect("/")
    hashword = bcrypt.generate_password_hash(request.form['password'])
    print(hashword)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashword
    }

    user_id = User.save(data)

    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')



@app.route("/login", methods=["POST"])
def login():
    data = {'email': request.form['log_email'],}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("invalid credentials", 'log_email')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['log_password']):
        flash("Invalid credentials", 'password')
        return redirect('/')
    return redirect('/dashboard')
    


@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('dashboard.html')
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
