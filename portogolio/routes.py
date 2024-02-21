#!/usr/bin/python3
"""starts an app flask"""

from flask import render_template, flash, redirect, url_for, abort
from flask import request
from flask_login import login_user, current_user, logout_user, login_required
from models import storage
from models.forms import (RegistrationForm,
                          LoginForm,
                          ProfileUpdateForm,
                          ProjectCreateForm,
                          CommentForm)
from models.comment import Comment
from models.profile import Profile
from models.projects import Project
from models.user import User
from models.tags import Tag

from models.utils import save_picture, format_skills
from portogolio import app, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)


@app.route("/", strict_slashes=False)
@app.route("/home", strict_slashes=False)
def home():
    """renders home page"""
    return render_template("home.html")


@app.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    """renders login page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.qurery_by_email(User, email=form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile', user_id=user.id))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", strict_slashes=False, methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('developers'))


@app.route("/profile/<user_id>", strict_slashes=False, methods=["GET", "POST"])
def profile(user_id):
    """renders profile page"""
    profile = storage.get_by_fk(Profile, user_id)
    user = storage.get(User, profile.user_id)
    projects = user.projects
    if current_user.is_authenticated and current_user.id == profile.user_id:
        form = ProfileUpdateForm()
        form.populate_tech_skills()

        if form.validate_on_submit():
            if form.profile_pic.data:
                picture_file = save_picture(form.profile_pic.data,
                                            "images",
                                            prev=current_user.profile_pic)
            else:
                picture_file = current_user.profile_pic

            tags = storage.get_tags(form.tech_skills.data)
            current_user.tags.clear()

            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.country = form.country.data
            current_user.role = form.role.data
            current_user.github = form.github.data
            current_user.linkedin = form.linkedin.data
            current_user.profile_pic = picture_file
            current_user.tags.extend(tags)
            storage.save()

            return redirect(url_for("profile", user_id=current_user.id))
        elif request.method == "GET":
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.country.data = current_user.country
            form.role.data = current_user.role
            form.github.data = current_user.github
            form.linkedin.data = current_user.linkedin
            form.tech_skills.data = current_user.tags


            picture_file = current_user.profile_pic
        return render_template('profile.html', user=current_user,
                               form=form,
                               is_authorized=True,
                               cll_1="profile-info",
                               cll_2="profile-container",
                               projects=projects)

    return render_template('profile.html', user=user,
                           is_authorized=False,
                           cll_1="profile-info-non",
                           cll_2="profile-container-non",
                           projects=projects)


@app.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register():
    """renders register page"""
    if current_user.is_authenticated:
        return redirect(url_for('developers'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    role=form.role.data,
                    github=form.github.data,
                    linkedin=form.linkedin.data,
                    country=form.country.data,
                    password=generate_password_hash(form.password.data))
        profile = Profile(user_id=user.id)
        storage.new(user)
        storage.new(profile)
        storage.save()

        flash('Your account has been created! You are now able to log in',
              'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/projects", strict_slashes=False)
def projects():
    """renders projects page"""
    projects = storage.all(Project).values()
    return render_template("projects.html", projects=projects)


@app.route("/profile/<user_id>/create_project",
           strict_slashes=False,
           methods=["GET", "POST"])
@login_required
def create_project(user_id):
    """renders create project page"""
    profile = storage.get_by_fk(Profile, user_id)
    if current_user.is_authenticated and current_user.id == profile.user_id:
        form = ProjectCreateForm()
        if form.validate_on_submit():

            project = Project(name=form.name.data,
                              description=form.description.data,
                              user_id=current_user.id,
                              tags=format_skills(form.tags.data),
                              github_link=form.github_link.data
                              )

            if form.background_image.data:
                picture_file = save_picture(form.background_image.data,
                                            "project_images",
                                            prev=project.background_image)
                project.background_image = picture_file
            storage.new(project)

            storage.save()
            flash('Project created successful', 'success')
            return redirect(url_for("show_project",
                                    user_id=user_id,
                                    project_id=project.id))

        return render_template("project.html",
                               form=form,
                               title="Create Project",
                               is_authorized=True)
    else:
        return abort(403)


@app.route("/profile/<user_id>/show/<project_id>",
           strict_slashes=False,
           methods=["GET", "POST"])
def show_project(user_id, project_id):
    """renders a singel project page"""
    profile = storage.get_by_fk(Profile, user_id)
    project = storage.get(Project, project_id)
    comments = storage.get_all_comments(project_id=project_id)

    if current_user.is_authenticated:
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data,
                              user_id=current_user.id,
                              project_id=project_id,
                              )
            storage.new(comment)
            storage.save()
            return redirect(url_for("show_project",
                                    user_id=user_id,
                                    project_id=project_id,
                                    ))
        return render_template("project.html",
                           form=form,
                           project=project,
                           comments=comments
                           )
    return render_template("project.html",
                           project=project,
                           comments=comments,
                           title=project.name)

@app.route("/profile/<user_id>/edit/<project_id>",
           strict_slashes=False,
           methods=["GET", "POST"])
@login_required
def edit_project(user_id, project_id):
    """renders form for editing project info"""
    profile = storage.get_by_fk(Profile, user_id)
    project = storage.get(Project, project_id)

    if current_user.is_authenticated and current_user.id == profile.user_id:
        form = ProjectCreateForm()
        if form.validate_on_submit():
            if form.background_image.data:
                picture_file = save_picture(form.background_image.data,
                                            "project_images",
                                            prev=project.background_image)
            else:
                picture_file = project.background_image
            print(form.tags.data)
            project.name = form.name.data
            project.description = form.description.data
            project.tags = format_skills(form.tags.data)
            project.github_link = form.github_link.data
            project.demo_link = form.demo_link.data
            project.background_image = picture_file
            storage.save()
            return redirect(url_for("show_project",
                                    user_id=user_id,
                                    project_id=project_id,
                                    ))
        elif request.method == "GET":
            form.name.data = project.name
            form.description.data = project.description
            form.github_link.data = project.github_link
            form.demo_link.data = project.demo_link
            form.tags.data = ','.join(project.tags)
            picture_file = project.background_image

            print(project.tags)

        return render_template("project.html", form=form,
                               project=project,
                               title="Edit project",
                               is_authorized=True)
    else:
        return abort(403)


@app.route("/profile/<user_id>/delete/<project_id>",
           strict_slashes=False,
           methods=["GET", "POST"])
@login_required
def delete_project(user_id, project_id):
    """renders a page to delet a project"""
    profile = storage.get_by_fk(Profile, user_id)
    project = storage.get(Project, project_id)
    if current_user.is_authenticated and current_user.id == profile.user_id:
        save_picture(None ,"project_images", project.background_image)
        storage.delete(project)
        storage.save()
        return redirect(url_for("profile", user_id=user_id))
    else:
        return abort(403)


@app.route("/developers", strict_slashes=False, methods=["GET", "POST"])
def developers():
    """renders developers page"""
    users = storage.all(User).values()
    return render_template("developers.html", users=users)
