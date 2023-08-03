#!/usr/bin/python3
"""
This script instantiates a storage object based on the environmental
 variable 'HBNB_TYPE_STORAGE'.
If 'HBNB_TYPE_STORAGE' is set to 'db',
it instantiates a database storage engine (DBStorage).
 Otherwise, it instantiates a file storage engine (FileStorage).
"""
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
