"""Flask App for Flask Cafe."""


from flask import Flask, render_template, request, flash
from flask import redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cafe, City, User
from forms import CafeForm, SignupForm, LoginForm, ProfileEditForm

from sqlalchemy.exc import IntegrityError

from secrets import FLASK_SECRET_KEY


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///flaskcafe'
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)


#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""
    # print("do_login app.py")
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def register_account():
    """Show signup form and process registration."""

    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        description = form.description.data
        email = form.email.data
        password = form.password.data
        image_url = form.image_url.data

        new_user = User.register(
            username,
            first_name,
            last_name,
            description,
            email,
            password,
            image_url or None
            )

        db.session.add(new_user)

        # put this in a try/ except IntegrityError
        # render the form again with an error message of "username already taken"
        try:
            
            db.session.commit()
            do_login(new_user)

            flash("You are signed up and logged in.")
            return redirect(f'/cafes')

        except IntegrityError:
            flash("Username already taken.")
            render_template('auth/signup-form.html', form=form)


    return render_template(
        'auth/signup-form.html', form=form
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Show signup form and process registration."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            do_login(user)
            flash(f'Hello, {username}')
            return redirect(f'/cafes')

        else:
            form.username.errors = ["Invalid credentials"]

    return render_template('auth/login-form.html', form=form)


@app.route("/logout", methods=["POST"])
def logout():
    """Logs user out and redirects to homepage."""

    do_logout()
    flash('successfully logged out')
    return redirect("/")


#######################################
# homepage

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes


@app.route('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )

@app.route('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )

@app.route('/cafes/add', methods=["GET", "POST"])
def add_cafe_form():
    """Show and process form for adding a new cafe. """

    form = CafeForm()
    cities = [(city.code, city.name) for city in City.query.all()]
    form.city_code.choices = cities

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        url = form.url.data
        address = form.address.data
        city_code = form.city_code.data
        image_url = form.image_url.data
    
        cafe = Cafe(
            name=name,
            description=description,
            url=url,
            address=address,
            city_code=city_code,
            image_url=image_url or None
        )

        db.session.add(cafe)
        db.session.commit()

        flash(f'{cafe.name} added')
        return redirect(f'/cafes/{cafe.id}')

    return render_template(
        'cafe/add-form.html', form=form
    )

@app.route('/cafes/<int:cafe_id>/edit', methods=["GET", "POST"])
def edit_cafe_form(cafe_id):
    """ Show and process form for editting cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)
    form = CafeForm(obj=cafe)
    cities = [(city.code, city.name) for city in City.query.all()]
    form.city_code.choices = cities

    if form.validate_on_submit():
        cafe.name = form.name.data
        cafe.description = form.description.data
        cafe.url = form.url.data
        cafe.address = form.address.data
        cafe.city_code = form.city_code.data
        cafe.image_url = form.image_url.data

        db.session.commit()

        flash(f'{cafe.name} edited.')
        return redirect(f'/cafes/{cafe.id}')

    return render_template(
        'cafe/edit-form.html', form=form, cafe=cafe
    )

#######################################
# User Data


@app.route('/profile')
def user_profile():
    """ If user logged in, show profile page. Otherwise, send to login."""
    if CURR_USER_KEY in session:
        return render_template('/profile/detail.html')
    else:
        return redirect('/login')


@app.route('/profile/edit', methods=["GET", "POST"])
def edit_user():
    """If user logged in, show and process form for editing user information.
    Otherwise, send to login page.
    """
    if CURR_USER_KEY in session:
        user = g.user
        form = ProfileEditForm(obj=user)

        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.description = form.description.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"

            db.session.commit()

            flash("Profile edited.")
            return redirect("/profile")

        return render_template('/profile/edit-form.html', form=form)
    else:
        return redirect('/login')