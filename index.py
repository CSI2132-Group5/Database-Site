from flask import (
    Flask, 
    request, 
    render_template,
    redirect,
    url_for
)

from flask_login import (
    login_user,
    logout_user,
    current_user,
    LoginManager
)
from flask_login.utils import login_required
from flask_wtf import CSRFProtect

from db import authenticate_user, fetch_user

app = Flask(__name__)
app.config.from_pyfile('config.py')

# settup the login authentication
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def get_user(ssn):
    db_response = fetch_user(ssn)
    return db_response

# protect our page from CSRF attempts
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        seed_phrase = request.form.get("seedphrase")
        
        user = authenticate_user(username=username, password=seed_phrase)
        # if we see a None value, the username is wrong
        if user is None:
            return render_template('login.html', wrong_password_or_user=True)
        else:
            # store the credentials and redirect to the dashboard
            login_user(user)
            return redirect(url_for('dashboard'))
    
    if current_user.is_authenticated:
        return redirect('dashboard')

    return render_template('login.html', wrong_password_or_user=False)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/admin/createuser')
@login_required
def createuser():
    return render_template("createuser.html")

if __name__ == "__main__":
    app.run()