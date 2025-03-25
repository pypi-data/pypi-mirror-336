import queue
import unittest
from FNA_DB.DBClient import DBClient
from TestServer import TestServer
import threading


class MyTestCase(unittest.TestCase):
    srv_thread = None
    client = None

    def setUp(self):
        test_server = TestServer()
        self.srv_thread = threading.Thread(target=test_server.run_server)
        self.srv_thread.start()
        self.client = DBClient()
        self.client.connect()
        super().setUp()

    def tearDown(self):
        self.client.close()
        self.srv_thread.join()

    def test_set_string_variable(self):
        self.assertEqual(self.client.set_value('Test1', 'Test1'), 'Test1')  # add assertion here

    def test_get_string_variable(self):
        self.client.set_value('Test2', 'Test2')
        self.assertEqual(self.client.get_value('Test2'), 'Test2')

    def test_set_int_variable(self):
        self.assertEqual(self.client.set_value('Test1', 5), 5)  # add assertion here

    def test_get_int_variable(self):
        self.client.set_value('Test2', 7)
        self.assertEqual(self.client.get_value('Test2'), 7)

    def test_set_bool_variable(self):
        self.assertEqual(self.client.set_value('Test1', True), True)  # add assertion here

    def test_get_bool_variable(self):
        self.client.set_value('Test2', False)
        self.assertEqual(self.client.get_value('Test2'), False)

    def test_set_float_variable(self):
        self.assertEqual(self.client.set_value('Test1', 10.225), 10.225)  # add assertion here

    def test_get_float_variable(self):
        self.client.set_value('Test2', 12.5)
        self.assertEqual(self.client.get_value('Test2'), 12.5)


if __name__ == '__main__':
    unittest.main()
