#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tiny_esa
# Copyright (C) 2018 Maxime Franco
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import unittest
import os
from tiny_esa.db_handler import db_handler
from tiny_esa.models import models


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.db_name = "db_handler_test.db"
        self.db = db_handler.ProjectDatabase(self.db_name)

    def tearDown(self):
        os.remove(self.db_name)

    def test_db_address(self):
        address = models.Address("street", "number", "postal_code", "city")
        self.db.add_address(address)
        self.assertEqual(self.db.get_address(), [(1, 'street', 'number', 'postal_code', 'city')])

        address.set_postal_code("cp")
        self.db.update_address(address)
        self.assertEqual(self.db.get_address(), [(1, 'street', 'number', 'cp', 'city')])

        self.db.remove_address(address)
        self.assertEqual(self.db.get_address(), [])

    def test_db_person(self):
        address = models.Address("street", "number", "postal_code", "city")
        test_person = models.Person(address, "last_name", "first_name", "gsm", "phone", "mail", "remark")
        self.db.add_person(test_person)
        self.assertEqual(self.db.get_address(), [(1, 'street', 'number', 'postal_code', 'city')])
        self.assertEqual(self.db.get_person(), [(1, 1, 'last_name', 'first_name', 'gsm', 'mail', 'phone', 'remark')])
        test_person.set_last_name("ln")
        test_person.set_first_name("fn")
        test_person.set_gsm("GSM")
        test_person.set_phone("PHONE")
        test_person.set_mail("email")
        test_person.set_remark("rmk")
        self.db.update_person(test_person)
        self.assertEqual(self.db.get_person(), [(1, 1, 'ln', 'fn', 'GSM', 'email', 'PHONE', 'rmk')])
        self.db.remove_person(test_person)
        self.assertEqual(self.db.get_address(), [])
        self.assertEqual(self.db.get_person(), [])

    def test_db_user(self):
        address = models.Address("street", "number", "postal_code", "city")
        person = models.Person(address, "last_name", "first_name", "gsm", "phone", "mail", "remark")
        user = models.User(person, "password", "12345")
        self.db.add_user(user)
        self.assertEqual(self.db.get_address(), [(1, 'street', 'number', 'postal_code', 'city')])
        self.assertEqual(self.db.get_person(), [(1, 1, 'last_name', 'first_name', 'gsm', 'mail', 'phone', 'remark')])
        tmp = self.db.get_user()
        sol = [(1, 1, "12345", 'edd1202f0851b877b47f11d727d586ccc967192c6f295518ff26ccb85f97e9a1')]
        for i in range(len(tmp[0])):
            self.assertEqual(tmp[0][i], sol[0][i])

        user.set_password("Password1")
        self.db.update_user(user)
        tmp = self.db.get_user()
        sol = [(1, 1, "12345", '18a196db9ead333356061b365ec9adbb272ae55e4cbae0253dff0e4726cb0dc1')]
        for i in range(len(tmp[0])):
            self.assertEqual(tmp[0][i], sol[0][i])


if __name__ == '__main__':
    unittest.main()
