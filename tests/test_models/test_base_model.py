#!/usr/bin/python3
""" Test of BaseModel  """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    def test_different_ids(self):
        """Test if two BaseModel instances have different ids"""
        i1 = self.value()
        i2 = self.value()
        self.assertNotEqual(i1.id, i2.id)

    def test_custom_uuid(self):
        """Test creating BaseModel instance with custom UUID"""
        custom_uuid = "550e8400-e29b-41d4-a716-446655440000"
        i = self.value(id=custom_uuid)
        self.assertEqual(i.id, custom_uuid)

    def test_created_at_update(self):
        """Test that created_at does not change on update"""
        i = self.value()
        created_at = i.created_at
        i.save()
        self.assertEqual(i.created_at, created_at)

    def test_updated_at_update(self):
        """Test that updated_at changes on update"""
        i = self.value()
        updated_at = i.updated_at
        i.save()
        self.assertNotEqual(i.updated_at, updated_at)

    def test_to_dict_type(self):
        """Test if the output of to_dict is a dictionary"""
        i = self.value()
        n = i.to_dict()
        self.assertIsInstance(n, dict)

    def test_to_dict_id(self):
        """Test if 'id' is present in the to_dict output"""
        i = self.value()
        n = i.to_dict()
        self.assertIn('id', n)

    def test_to_dict_created_at(self):
        """Test if 'created_at' is present in the to_dict output"""
        i = self.value()
        n = i.to_dict()
        self.assertIn('created_at', n)

    def test_to_dict_updated_at(self):
        """Test if 'updated_at' is present in the to_dict output"""
        i = self.value()
        n = i.to_dict()
        self.assertIn('updated_at', n)

    def test_from_dict(self):
        """Test if from_dict creates a BaseModel instance correctly"""
        data = {
            'id': '550e8400-e29b-41d4-a716-446655440000',
            'created_at': '2023-08-04T12:00:00',
            'updated_at': '2023-08-04T12:30:00',
            'custom_attribute': 'test_value'
        }
        i = self.value.from_dict(data)
        self.assertEqual(i.id, data['id'])
        self.assertEqual(str(i.created_at), data['created_at'])
        self.assertEqual(str(i.updated_at), data['updated_at'])
        self.assertEqual(i.custom_attribute, data['custom_attribute'])

    def test_from_dict_invalid_data(self):
        """Test if from_dict handles invalid data correctly"""
        data = {'invalid_key': 'invalid_value'}
        with self.assertRaises(ValueError):
            i = self.value.from_dict(data)

if __name__ == '__main__':
    unittest.main()
