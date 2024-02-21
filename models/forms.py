#!/usr/bin/python3
"""This module defines a class RegistrationFormser and LoginForm"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from models import storage
from wtforms import (StringField,
                     PasswordField,
                     SubmitField,
                     BooleanField,
                     TextAreaField,
                     URLField,
                     SelectMultipleField,
                     widgets)
from wtforms.validators import (DataRequired,
                                Length,
                                Email,
                                EqualTo,
                                ValidationError,
                                URL,
                                Optional)
from models.user import User
from models.tags import Tag



class CustomSelectMultipleField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    role = StringField('Role', validators=[DataRequired(),
                                           Length(min=2, max=20)])
    country = StringField('Country', validators=[DataRequired(),
                                           Length(min=2, max=20)])
    github = URLField('Github',
                           validators=[DataRequired(), URL()])
    linkedin = URLField('Linkedin',
                           validators=[DataRequired(), URL()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = storage.qurery_by_name(User, username.data)
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        user = storage.qurery_by_email(User, email.data)
        if user:
            raise ValidationError('Email already exists.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ProfileUpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    role = StringField('Role', validators=[DataRequired(),
                                           Length(min=2, max=20)])

    profile_pic = FileField('Profile pic',
                            validators=[FileAllowed(['jpg', 'png'])])
    country = StringField('Contry',
                           validators=[DataRequired(), Length(max=20)])
    github = URLField('Github',
                           validators=[DataRequired(), URL()])
    linkedin = URLField('Linkedin',
                           validators=[DataRequired(), URL()])
    tech_skills = CustomSelectMultipleField('Tech Stack',
                                    coerce=str,
                                    choices=[])
    additional_skills = StringField('Additional Skills')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = storage.qurery_by_name(User, username.data)
            if user:
                raise ValidationError('Username already exists.')

    def validate_email(self, email):
        if email.data != current_user.email:

            user = storage.qurery_by_email(User, email.data)
            if user:
                raise ValidationError('Email already exists.')

    def populate_tech_skills(self):
        print("errt")
        self.tech_skills.choices = [(str(skill.name), skill.name) for skill in storage.all(Tag).values()]



class ProjectCreateForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    github_link = URLField('Github',
                           validators=[DataRequired(), URL()])
    demo_link = URLField('Demo',
                           validators=[Optional(), URL()])
    description = TextAreaField('Description',
                        validators=[DataRequired(), Length(min=2, max=2000)])
    background_image = FileField('Background image',
                                 validators=[FileAllowed(['jpg', 'png'])])
    tags = StringField("Tags ('comma-separated')", validators=[DataRequired()])
    submit = SubmitField('Save')


class CommentForm(FlaskForm):
    body = StringField('Body', validators=[DataRequired(Length(max=512))])
    submit = SubmitField('Post')