#!/user/bin/python3
"""
This module for helper functions
"""
from flask import current_app
import os
from PIL import Image
import secrets


def save_picture(form_picture, path, prev=None):
    """
    save new image to storage and return it's path or
    delete an images if a new one is uploaded
    """
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


def paginate_query(query, page_number, project_count):
    """
    Function that return list of instances result paginated or empty list
    """
    page_size = 5

    totat_pages = (project_count // page_size) + (project_count % page_size)
    if totat_pages == 0:
        return [], totat_pages, page_size

    if page_number < 1:
        page_number = 1

    if page_number > totat_pages:
        page_number = totat_pages
    if project_count <= page_size:
        totat_pages = 1
    print(page_number)
    offset = (page_number - 1) * page_size
    return (query.slice(offset, offset + page_size).all(),
            totat_pages,
            page_size)
