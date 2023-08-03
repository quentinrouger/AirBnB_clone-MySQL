#!/usr/bin/python3
"""
This script defines the FileStorage class, an abstracted storage engine.
"""
import json
from models.base_model import BaseModel, Amenity, City
from models.base_model import  Place, Review, State, User


class FileStorage:
    """
    Represents an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Return a dictionary of instantiated objects in __objects.

        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            cls_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    cls_dict[key] = value
            return cls_dict
        return self.__objects

    def new(self, obj):
        """
        Set in __objects obj with key <obj_class_name>.id.
        """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """
        Serialize __objects to the JSON file __file_path.
        """
        serialized_objects = {key: value.to_dict()
                              for key, value in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
        Deserialize the JSON file __file_path to __objects, if it exists.
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                loaded_objects = json.load(file)
                for key, value in loaded_objects.items():
                    class_name = value["__class__"]
                    del value["__class__"]
                    self.new(eval(class_name)(**value))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Delete a given object from __objects, if it exists.
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(key, None)

    def close(self):
        """
        Call the reload method.
        """
        self.reload()
