import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage


class TestHBNBCommand(unittest.TestCase):

    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        storage.delete_all()

    def test_do_create(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('create BaseModel')
            obj_id = output.getvalue().strip()
        self.assertIsNotNone(storage.get('BaseModel', obj_id))

    def test_do_show(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('create BaseModel')
            obj_id = output.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd(f'show BaseModel {obj_id}')
            expected_output = f'[{obj_id}] BaseModel {storage.get("BaseModel",
                                                                  obj_id)}'
            self.assertEqual(output.getvalue().strip(), expected_output)

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('show BaseModel fake_id')
            expected_output = "** no instance found **"
            self.assertEqual(output.getvalue().strip(), expected_output)

    def test_do_destroy(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('create BaseModel')
            obj_id = output.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd(f'destroy BaseModel {obj_id}')
            self.assertEqual(output.getvalue().strip(), '')
        self.assertIsNone(storage.get('BaseModel', obj_id))

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('destroy BaseModel fake_id')
            expected_output = "** no instance found **"
            self.assertEqual(output.getvalue().strip(), expected_output)

    def test_do_all(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('create BaseModel')
            obj_id1 = output.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('create BaseModel')
            obj_id2 = output.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('all')
            expected_output =\
            f'[{obj_id1}] BaseModel {storage.get("BaseModel", obj_id1)}\n' \
                f'[{obj_id2}] BaseModel {storage.get("BaseModel", obj_id2)}'
            self.assertEqual(output.getvalue().strip(), expected_output)

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('all FakeModel')
            expected_output = "** class doesn't exist **"
            self.assertEqual(output.getvalue().strip(), expected_output)

    def test_do_update(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('create BaseModel')
            obj_id = output.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd(f'update BaseModel {obj_id} name "New Name"')
            self.assertEqual(output.getvalue().strip(), '')
        obj = storage.get('BaseModel', obj_id)
        self.assertEqual(obj.name, "New Name")

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('update BaseModel fake_id')
            expected_output = "** no instance found **"
            self.assertEqual(output.getvalue().strip(), expected_output)

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('update BaseModel')
            expected_output = "** class name missing **"
            self.assertEqual(output.getvalue().strip(), expected_output)


if __name__ == '__main__':
    unittest.main()
