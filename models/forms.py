#!/usr/bin/python3
"""This module defines a class RegistrationFormser and LoginForm"""


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField,
                     PasswordField,
                     SubmitField,
                     BooleanField,
                     TextAreaField)
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    role = StringField('Role', validators=[DataRequired(),
                                           Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')


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
                           validators=[Length(max=20)])
    submit = SubmitField('Update')


class ProjectCreateForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    github_link = StringField('Github',
                           validators=[DataRequired(), Length(min=2, max=128)])
    demo_link = StringField('Demo',
                           validators=[Length(max=128)])
    description = TextAreaField('Description',
                        validators=[DataRequired(), Length(min=2, max=2000)])
    background_image = FileField('Background image',
                                 validators=[FileAllowed(['jpg', 'png'])])
    tags = StringField("Tags ('comma-separated')", validators=[DataRequired()])
    submit = SubmitField('Save')


class CommentForm(FlaskForm):
    body = StringField('Body', validators=[DataRequired(Length(max=512))])
    submit = SubmitField('Post')
