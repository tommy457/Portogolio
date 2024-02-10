#!/user/bin/python3
"""
This module for helper functions
"""
import os
from PIL import Image
import secrets


def save_picture(form_picture, path, app, prev=None):
    if prev and prev != "default.jpg":
        os.remove(path='static/{}/{}'.format(path, prev))
    print("IN")
    if form_picture:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path,
                                    'static/{}'.format(path),
                                    picture_fn)

        output_size = (900, 900)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        print("saved")
        return picture_fn

def format_skills(data):
    """helper function for formatting text"""
    skills = data
    print(skills.split())
    skills_list = [skill.strip() for skill in skills.split(',')]
    return skills_list