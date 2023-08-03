#!/usr/bin/python3

import json




class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
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
        Returns a dictionary of objects in the storage
        Args:
            cls (class): The class to filter the objects by.
        Returns:
            dict: A dictionary of objects filtered by class name.
        Return a dictionary of instantiated objects in __objects.
        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is None:
            return self.__objects
        else:
            objects_by_class = {}
            for obj_id, obj in self.__objects.items():
                if type(obj) == cls:
                    objects_by_class[obj_id] = obj
            return objects_by_class
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
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})
        """
        Set in __objects obj with key <obj_class_name>.id.
        """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)
        """
        Serialize __objects to the JSON file __file_path.
        """
        serialized_objects = {key: value.to_dict()
                              for key, value in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        """
        Deserialize the JSON file __file_path to __objects, if it exists.
        """
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
            with open(self.__file_path, "r", encoding="utf-8") as file:
                loaded_objects = json.load(file)
                for key, value in loaded_objects.items():
                    class_name = value["__class__"]
                    del value["__class__"]
                    self.new(eval(class_name)(**value))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete an object from __objects if it exists.
        Args:
            obj (BaseModel): The object to delete. If set to None, do nothing.
        Returns:
            None
        """
        if obj is None:
            return
        """
        Delete a given
        object from __objects, if it exists.
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(key, None)

        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        if key in self.__objects:
            del self.__objects[key]
            self.save()
    def close(self):
        """
        Call the reload method.
        """
        self.reload()
