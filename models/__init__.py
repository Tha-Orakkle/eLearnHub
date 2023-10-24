#!/usr/bin/python3
"""initializes the models package"""
from os import environ


storage_type = environ.get('ELH_STORAGE_TYPE')
if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()