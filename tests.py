'''
-tests do not pass-
TODO: update to /api/v1/*

example 1 - FAIL
example 2 - PASS
example 3 - PASS
example 4 - PASS
example 5 - PASS
example 6 - PASS
'''
import unittest
import base64
import json
from datetime import datetime

from peewee import *
from werkzeug.exceptions import NotFound

import pdapt
import config
import models
from resources import guid

CLIENT = pdapt.app.test_client()


# TESTS GO HERE
class A_ModelsTestCase(unittest.TestCase):
    def test_A_initialize(self):
        models.initialize()
        for mdobj in pdapt.models.MdObj.select():
            mdobj.delete_instance()

    def test_B_create_mdobj(self):
        # at this point, the database should be empty
        self.assertEqual(pdapt.models.MdObj.select().count(), 0)
        mdobj = models.MdObj.create(user="TestRunner")
        self.assertEqual(pdapt.models.MdObj.select().count(), 1)
        with self.assertRaises(NotFound):
            mdobj = guid.get_mdobj_or_404(1)
        mdobj.delete_instance()

    def test_C_get_or_404(self):
        with self.assertRaises(NotFound):
            guid.get_mdobj_or_404("8BBB25CF671C4252A10ACE550A29C890")
        models.MdObj.create(
            guid="8BBB25CF671C4252A10ACE550A29C890", user="Cylance, Inc.`")
        self.assertEqual(guid.get_mdobj_or_404(
            "8BBB25CF671C4252A10ACE550A29C890").guid,
            '8BBB25CF671C4252A10ACE550A29C890')

    def test_ZZ_tearDown(self):
        for mdobj in pdapt.models.MdObj.select():
            mdobj.delete_instance()


class B_MdObjTestResources(unittest.TestCase):
    def test_A_ViewRoutes(self):
        rv = CLIENT.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_B_MdObjAPIRoutes_Put_invalidGUID(self):
        rv = CLIENT.put(
            '/guid/9094E4C980C74043A4B586B420E.')
        self.assertEqual(rv.status_code, 400)
        rv = CLIENT.put(
            '/guid/9094E4C980C74043A4B586B420E69ddf')
        self.assertEqual(rv.status_code, 400)
        rv = CLIENT.put(
            '/guid/9094E4C980C74043A4B586B420E&*DDF')
        self.assertEqual(rv.status_code, 400)

    def test_B_MdObjAPIRoutes_Put_wID(self):
        # example 1
        rv = CLIENT.put(
            '/guid/9094E4C980C74043A4B586B420E69DDF?user=Cylance, Inc.')
        self.assertEqual(rv.status_code, 201)

        # example 3
        rv = CLIENT.get(
            '/guid/9094E4C980C74043A4B586B420E69DDF')
        self.assertEqual(rv.status_code, 200)

    def test_C_MdObjAPIRoutes_Put_WoID(self):
        # example 2
        rv = CLIENT.put('/guid?user=Cylance, Inc.')
        self.assertEqual(rv.status_code, 201)

    def test_D_MdObjAPIRoutes_Put_update(self):
        # example 4
        rv = CLIENT.put(
            '/guid/9094E4C980C74043A4B586B420E69DDF?expire=1427822745')
        self.assertEqual(rv.status_code, 200)

    def test_D_MdObjAPIRoutes_Put_invalidUpdate(self):
        rv = CLIENT.put(
            '/guid/9094E4C980C74043A4B586B420E69DDF?expire=12/31/1999')
        self.assertEqual(rv.status_code, 400)

    def test_E_MdObjAPIRoutes_Delete(self):
        # example 5
        rv = CLIENT.delete('/guid/9094E4C980C74043A4B586B420E69DDF')
        self.assertEqual(rv.status_code, 204)


# Run all Tests
if __name__ == '__main__':
    # load tests from TestResources
    suite = unittest.TestLoader().loadTestsFromTestCase(
        A_ModelsTestCase)
    # load tests from ModelsTestCase
    suite.addTest(unittest.TestLoader(
    ).loadTestsFromTestCase(B_MdObjTestResources))
    unittest.TextTestRunner(verbosity=2).run(suite)
