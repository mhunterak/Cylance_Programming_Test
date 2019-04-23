import unittest
import base64
import json
from datetime import datetime

from peewee import *
from werkzeug.exceptions import NotFound

import pdapt
import config
import models

CLIENT = pdapt.app.test_client()


# TESTS GO HERE
class A_ModelsTestCase(unittest.TestCase):
    def test_A_initialize(self):
        models.initialize()
        for mdobj in models.MdObj.select():
            mdobj.delete_instance()

    def test_B_create_mdobj(self):
        # at this point, the database should be empty
        self.assertEqual(models.MdObj.select().count(), 0)
        mdobj = models.MdObj.create(user="TestRunner")
        self.assertEqual(models.MdObj.select().count(), 1)
        mdobj.delete_instance()
        with self.assertRaises(NotFound):
            mdobj = pdapt.get_mdobj_or_404(mdobj.guid)

    def test_C_get_or_404(self):
        with self.assertRaises(NotFound):
            pdapt.get_mdobj_or_404("8BBB25CF671C4252A10ACE550A29C890")
        models.MdObj.create(
            guid="8BBB25CF671C4252A10ACE550A29C890", user="Cylance, Inc.`")
        self.assertEqual(pdapt.get_mdobj_or_404(
            "8BBB25CF671C4252A10ACE550A29C890").guid,
            '8BBB25CF671C4252A10ACE550A29C890')

    def test_ZZ_tearDown(self):
        for mdobj in models.MdObj.select():
            mdobj.delete_instance()


class B_MdObjTestResources(unittest.TestCase):
    def test_A_ViewRoutes(self):
        rv = CLIENT.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_B_MdObjAPIRoutes_Put_invalidGUID(self):
        '''
        This function tests invalid routes
        '''
        rv = CLIENT.post(
            '/api/v1/guid/9094E4C980C74043A4B586B420E.',
            data="""{
                "expire": "1427736345",
                "user": "Cylance, Inc."
            }
            """,
            content_type='application/json')
        self.assertEqual(rv.status_code, 400)
        rv = CLIENT.post(
            '/api/v1/guid/9094E4C980C74043A4B586B420E69ddf',
            data="""{
                "expire": "1427736345",
                "user": "Cylance, Inc."
            }
            """,
            content_type='application/json')
        self.assertEqual(rv.status_code, 400)
        rv = CLIENT.post(
            '/api/v1/guid/9094E4C980C74043A4B586B420E&*DDF',
            data="""{
                "expire": "1427736345",
                "user": "Cylance, Inc."
            }
            """,
            content_type='application/json')
        self.assertEqual(rv.status_code, 400)

    def test_B_MdObjAPIRoutes_Put_wID(self):
        # example 1
        rv = CLIENT.post(
            '/api/v1/guid/9094E4C980C74043A4B586B420E69DDF',
            data="""{
                "expire": "1427736345",
                "user": "Cylance, Inc."
            }
            """,
            content_type='application/json')
        self.assertEqual(rv.status_code, 201)

        # example 3
        rv = CLIENT.get(
            '/api/v1/guid/9094E4C980C74043A4B586B420E69DDF',
            # data=<< << << <<
            content_type='application/json')
        self.assertEqual(rv.status_code, 200)

    def test_C_MdObjAPIRoutes_Put_WoID(self):
        # example 2
        rv = CLIENT.post(
            '/api/v1/guid',
            data="""{"user": "Cylance, Inc."}""",
            content_type='application/json')
        self.assertEqual(rv.status_code, 201)

    def test_D_MdObjAPIRoutes_Put_update(self):
        # example 4
        rv = CLIENT.post(
            '/api/v1/guid/9094E4C980C74043A4B586B420E69DDF',
            # data=<< << << <<
            data="""{
                "expire": "1427736125",
                "user": "Cylance, Inc."
            }
            """,
            content_type='application/json')
        self.assertEqual(rv.status_code, 200)

    def test_D_MdObjAPIRoutes_Put_invalidUpdate(self):
        rv = CLIENT.post(
            '/api/v1/guid/9094E4C980C74043A4B586B420E69DDF',
            data="""{
                "expire": "2/31/1999",
            }
            """,
            content_type='application/json')
        self.assertEqual(rv.status_code, 400)

    def test_E_MdObjAPIRoutes_Delete(self):
        # example 5
        rv = CLIENT.delete('/api/v1/guid/9094E4C980C74043A4B586B420E69DDF',
                           content_type='application/json')
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
