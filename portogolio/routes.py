#!/usr/bin/python3
"""route for portogolio flask app"""

from flask import render_template, flash, redirect, url_for, abort
from flask import request
from flask_login import login_user, current_user, logout_user, login_required
from models import storage
from models.forms import (
    RegistrationForm,
    LoginForm,
    ProfileUpdateForm,
    ProjectCreateForm,
    CommentForm,
    SeachForm,
)
from models.comment import Comment
from models.profile import Profile
from models.projects import Project
from models.user import User
from models.tags import Tag
from flask_paginate import Pagination
from models.utils import save_picture, paginate_query
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
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.qurery_by_email(User, email=form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("profile", user_id=user.id))
        else:
            flash("Login Unsuccessful. Please check email and password",
                  "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", strict_slashes=False, methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("developers"))


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
                picture_file = save_picture(
                    form.profile_pic.data,
                    "images",
                    prev=current_user.profile_pic
                )
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
        return render_template(
            "profile.html",
            user=current_user,
            form=form,
            is_authorized=True,
            cll_1="profile-info",
            cll_2="profile-container",
            projects=projects,
        )

    return render_template(
        "profile.html",
        user=user,
        is_authorized=False,
        cll_1="profile-info-non",
        cll_2="profile-container-non",
        projects=projects,
    )


@app.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register():
    """renders register page"""
    if current_user.is_authenticated:
        return redirect(url_for("developers"))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data.title(),
            email=form.email.data,
            role=form.role.data,
            github=form.github.data,
            linkedin=form.linkedin.data,
            country=form.country.data,
            password=generate_password_hash(form.password.data),
        )
        profile = Profile(user_id=user.id)
        storage.new(user)
        storage.new(profile)
        storage.save()

        flash("Your account has been created! You are now able to log in",
              "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/projects", strict_slashes=False, methods=["GET", "POST"])
def projects():
    """renders projects page"""
    form = SeachForm()
    form.populate_tech_skills()
    page_number = int(request.args.get('page_number', 1))
    tags = request.args.get("tags")
    query, project_count = storage.get_query(Project)

    if form.validate_on_submit():
        if form.tags.data:
            query, project_count = storage.filter_projects(form.tags.data)
            tags = form.tags.data
    elif tags:
        query, project_count = storage.filter_projects([tags])

    projects, total_pages, page_size = paginate_query(query,
                                                      page_number,
                                                      project_count)
    if page_number > total_pages:
        page_number = 1
    return render_template(
        "projects.html",
        projects=projects,
        form=form,
        page_number=page_number,
        total_pages=total_pages,
        project_count=project_count,
        page_size=page_size,
        tags=tags,
        )


@app.route(
    "/profile/<user_id>/create_project",
    strict_slashes=False,
    methods=["GET", "POST"]
)
@login_required
def create_project(user_id):
    """renders create project page"""
    profile = storage.get_by_fk(Profile, user_id)
    if current_user.is_authenticated and current_user.id == profile.user_id:
        form = ProjectCreateForm()
        form.populate_tech_skills()

        if form.validate_on_submit():

            project = Project(
                name=form.name.data,
                description=form.description.data,
                user_id=current_user.id,
                github_link=form.github_link.data,
            )
            tags = storage.get_tags(form.tech_skills.data)
            project.tags.extend(tags)

            # save new image and return it's path
            # same for db_image and infra_image
            if form.background_image.data:
                picture_file = save_picture(
                    form.background_image.data,
                    "project_images",
                    prev=project.background_image,
                )
                project.background_image = picture_file

            if form.db_image.data:
                db_image = save_picture(
                    form.db_image.data, "project_images", prev=project.db_image
                )
                project.db_image = db_image

            if form.infra_image.data:
                infra_image = save_picture(
                    form.infra_image.data,
                    "project_images",
                    prev=project.infra_image
                )
                project.infra_image = infra_image

            storage.new(project)

            storage.save()
            flash("Project created successful", "success")
            return redirect(
                url_for("show_project", user_id=user_id, project_id=project.id)
            )

        return render_template(
            "project.html",
            form=form, title="Create Project",
            is_authorized=True
        )
    else:
        return abort(403)


@app.route(
    "/profile/<user_id>/show/<project_id>",
    strict_slashes=False,
    methods=["GET", "POST"],
)
def show_project(user_id, project_id):
    """renders a singel project page"""
    project = storage.get(Project, project_id)
    comments = storage.get_all_comments(project_id=project_id)

    if current_user.is_authenticated:
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(
                body=form.body.data,
                user_id=current_user.id,
                project_id=project_id,
            )
            storage.new(comment)
            storage.save()
            return redirect(
                url_for(
                    "show_project",
                    user_id=user_id,
                    project_id=project_id,
                )
            )
        return render_template(
            "project.html", form=form, project=project, comments=comments
        )
    return render_template(
        "project.html", project=project, comments=comments, title=project.name
    )


@app.route(
    "/profile/<user_id>/edit/<project_id>",
    strict_slashes=False,
    methods=["GET", "POST"],
)
@login_required
def edit_project(user_id, project_id):
    """renders form for editing project info"""
    profile = storage.get_by_fk(Profile, user_id)
    project = storage.get(Project, project_id)

    if current_user.is_authenticated and current_user.id == profile.user_id:
        form = ProjectCreateForm()
        form.populate_tech_skills()

        if form.validate_on_submit():
            # update and remove previous image and save new image
            # return the path to the saved image
            # same for db_image and infra_image
            if form.background_image.data:
                picture_file = save_picture(
                    form.background_image.data,
                    "project_images",
                    prev=project.background_image,
                )
            else:
                picture_file = project.background_image

            if form.db_image.data:
                db_image = save_picture(
                    form.db_image.data, "project_images", prev=project.db_image
                )
            else:
                db_image = project.db_image
            if form.infra_image.data:
                infra_image = save_picture(
                    form.infra_image.data,
                    "project_images",
                    prev=project.infra_image
                )
            else:
                infra_image = project.infra_image
            tags = storage.get_tags(form.tech_skills.data)
            project.tags.clear()

            project.name = form.name.data
            project.description = form.description.data
            project.tags.extend(tags)
            project.github_link = form.github_link.data
            project.demo_link = form.demo_link.data
            project.background_image = picture_file
            project.db_image = db_image
            project.infra_image = infra_image

            storage.save()
            return redirect(
                url_for(
                    "show_project",
                    user_id=user_id,
                    project_id=project_id,
                )
            )
        # show current project info if it's not a POST request
        elif request.method == "GET":
            form.name.data = project.name
            form.description.data = project.description
            form.github_link.data = project.github_link
            form.demo_link.data = project.demo_link
            form.tech_skills.data = project.tags
            picture_file = project.background_image
            db_image = project.db_image
            infra_image = project.infra_image

            print(project.tags)

        return render_template(
            "project.html",
            form=form,
            project=project,
            title="Edit project",
            is_authorized=True,
        )
    else:
        return abort(403)


@app.route(
    "/profile/<user_id>/delete/<project_id>",
    strict_slashes=False,
    methods=["GET", "POST"],
)
@login_required
def delete_project(user_id, project_id):
    """renders a page to delet a project"""
    profile = storage.get_by_fk(Profile, user_id)
    project = storage.get(Project, project_id)
    if current_user.is_authenticated and current_user.id == profile.user_id:
        # clean up project images before project is deleted
        save_picture(None, "project_images", project.background_image)
        save_picture(None, "project_images", project.db_image)
        save_picture(None, "project_images", project.infra_image)

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