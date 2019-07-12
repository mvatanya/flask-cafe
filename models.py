"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = 'cities'

    code = db.Column(
        db.Text,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    state = db.Column(
        db.String(2),
        nullable=False,
    )


class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = 'cafes'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    url = db.Column(
        db.Text,
        nullable=False,
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )

    city_code = db.Column(
        db.Text,
        db.ForeignKey('cities.code'),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-cafe.jpg",
    )

    city = db.relationship("City", backref='cafes')

    likes = db.relationship('Like')
    liking_users = db.relationship('User', secondary='likes', backref="liked_cafes")

    def __repr__(self):
        return f'<Cafe id={self.id}, name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f'{city.name}, {city.state}'


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True)

    email = db.Column(db.Text)

    first_name = db.Column(
        db.Text,
        nullable=False)

    last_name = db.Column(
        db.Text,
        nullable=False)

    description = db.Column(db.Text)

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-pic.png")
  
    hashed_password = db.Column(
        db.Text,
        nullable=False)

    admin = db.Column(
        db.Boolean,
        default=False)

    likes = db.relationship('Like') 
    

    def get_full_name(self):
        """ Get full name of user """

        return f'{self.first_name} {self.last_name}'
    
    def __repr__(self):
        u = self
        return f"<User: {u.id}, {u.username}, {u.admin}, {u.email}, {u.first_name}, {u.last_name}>"



    @classmethod
    def register(
            cls,
            username,
            first_name,
            last_name,
            description,
            email,
            password,
            image_url="/static/images/default-pic.png",
            admin=False):

        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed password
        return cls(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            description=description,
            image_url=image_url,
            hashed_password=hashed_utf8,
            admin=admin)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.hashed_password, pwd):
            # return user instance
            return u
        else:
            return False


class Like(db.Model):
    """Mapping of a cafe to a user"""

    __tablename__ = "likes"

    cafe_id = db.Column(
                db.Integer,
                db.ForeignKey("cafes.id"),
                primary_key=True)

    user_id = db.Column(
                db.Integer,
                db.ForeignKey("users.id"),
                primary_key=True)

    def __repr__(self):
        like = self
        return f"<Like: {like.cafe_id}, {like.user_id}>"

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)






