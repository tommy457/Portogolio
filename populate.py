#!/usr/bin/python3
from models.tags import Tag
from models import storage



skills = ['Python', 'Javascrip', 'Flask', 'NodeJs', 'Django']

for name in skills:
    new_tag = Tag(name=name)
    storage.new(new_tag)
    storage.save()