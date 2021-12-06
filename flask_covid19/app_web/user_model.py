from flask_covid19.app_config.database import db, items_per_page
from flask_login import UserMixin, AnonymousUserMixin
from wtforms import validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField


class User(UserMixin, db.Model):
    __tablename__ = 'usr'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode(512), nullable=False, unique=True)
    password_hash = db.Column(db.String(2048), nullable=False)
    name = db.Column(db.String(512), nullable=False)

    @classmethod
    def create_new(cls, email, name: str, password_hash: str):
        return User(
            email=email,
            name=name,
            password_hash=password_hash)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def count(cls):
        return db.session.query(cls).count()

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).paginate(page, per_page=items_per_page)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_by_id(cls, other_id):
        my_other_id = int(other_id)
        return db.session.query(cls).filter(cls.id == my_other_id).one_or_none()


class AnonymousUserValueObject(AnonymousUserMixin):
    pass


class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email(), validators.InputRequired()])
    password = PasswordField('Password', [validators.Length(min=6, max=35), validators.InputRequired()])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

    def validate_on_submit(self):
        if self.email is None:
            return False
        if self.password is None:
            return False
        if self.accept_rules is None:
            return False
        return True

