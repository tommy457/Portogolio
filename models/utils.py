#!/user/bin/python3
"""
This module for helper functions
"""
from flask import current_app
import os
from PIL import Image
import secrets


def save_picture(form_picture, path, prev=None):
    if prev and prev != "default.png":
        os.remove(
            path=os.path.join(current_app.root_path,
                              "static/{}/{}".format(path, prev))
        )

    if form_picture:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(
            current_app.root_path, "static/{}".format(path), picture_fn
        )

        if path == "images":
            output_size = (134, 134)
        elif path == "project_images":
            output_size = (900, 600)

        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        print("saved")
        return picture_fn
