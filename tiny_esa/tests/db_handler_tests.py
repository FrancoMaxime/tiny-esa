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

        address.postal_code = "cp"
        self.db.update_address(address)
        self.assertEqual(self.db.get_address(), [(1, 'street', 'number', 'cp', 'city')])

        self.db.remove_address(address)
        self.assertEqual(self.db.get_address(), [])

    def test_db_person(self):
        address = models.Address("street", "number", "postal_code", "city")
        test_person = models.Person(address, "last_name", "first_name", "gsm", "phone", "mail", "12345", "remark")
        self.db.add_person(test_person)
        self.assertEqual(self.db.get_address(), [(1, 'street', 'number', 'postal_code', 'city')])
        self.assertEqual(self.db.get_person(), [(1, 1, 'last_name', 'first_name', 'gsm', 'mail', 'phone', '12345', "remark")])
        test_person.last_name = "ln"
        test_person.first_name = "fn"
        test_person.gsm = "GSM"
        test_person.phone = "PHONE"
        test_person.mail = "email"
        test_person.remark = "rmk"
        self.db.update_person(test_person)
        self.assertEqual(self.db.get_person(), [(1, 1, 'ln', 'fn', 'GSM', 'email', 'PHONE', "12345", 'rmk')])
        self.db.remove_person(test_person)
        self.assertEqual(self.db.get_address(), [])
        self.assertEqual(self.db.get_person(), [])

    def test_db_user(self):
        address = models.Address("street", "number", "postal_code", "city")
        person = models.Person(address, "last_name", "first_name", "gsm", "phone", "mail", "12345","remark")
        user = models.User(person, "password")
        self.db.add_user(user)
        self.assertEqual(self.db.get_address(), [(1, 'street', 'number', 'postal_code', 'city')])
        self.assertEqual(self.db.get_person(), [(1, 1, 'last_name', 'first_name', 'gsm', 'mail', 'phone', "12345",'remark')])
        tmp = self.db.get_user()
        sol = [(1, 1, 'edd1202f0851b877b47f11d727d586ccc967192c6f295518ff26ccb85f97e9a1')]
        for i in range(len(tmp[0])):
            self.assertEqual(tmp[0][i], sol[0][i])

        user.password = "Password1"
        self.db.update_user(user)
        tmp = self.db.get_user()
        sol = [(1, 1, '18a196db9ead333356061b365ec9adbb272ae55e4cbae0253dff0e4726cb0dc1')]
        for i in range(len(tmp[0])):
            self.assertEqual(tmp[0][i], sol[0][i])
        self.db.remove_user(user)
        self.assertEqual(self.db.get_address(), [])
        self.assertEqual(self.db.get_person(), [])
        self.assertEqual(self.db.get_user(), [])

    def test_db_customer(self):
        address = models.Address("street", "number", "postal_code", "city")
        person = models.Person(address, "last_name", "first_name", "gsm", "phone", "mail", "12345", "remark")
        customer = models.Customer(person, "evaluation")
        self.db.add_customer(customer)
        self.assertEqual(self.db.get_address(), [(1, 'street', 'number', 'postal_code', 'city')])
        self.assertEqual(self.db.get_person(), [(1, 1, 'last_name', 'first_name', 'gsm', 'mail', 'phone', "12345", 'remark')])
        tmp = self.db.get_customer()
        sol = [(1, 1, 'evaluation')]
        for i in range(len(tmp[0])):
            self.assertEqual(tmp[0][i], sol[0][i])

        customer.evaluation = "EVAL"
        self.db.update_customer(customer)
        tmp = self.db.get_customer()
        sol = [(1, 1, 'EVAL')]
        for i in range(len(tmp[0])):
            self.assertEqual(tmp[0][i], sol[0][i])
        self.db.remove_customer(customer)
        self.assertEqual(self.db.get_address(), [])
        self.assertEqual(self.db.get_person(), [])
        self.assertEqual(self.db.get_customer(), [])

    def test_db_company(self):
        address_u = models.Address("street_u", "number_u", "postal_code_u", "city_u")
        address_c = models.Address("street_c", "number_c", "postal_code_c", "city_c")
        person = models.Person(address_u, "last_name", "first_name", "gsm", "phone", "mail", "12345", "remark")
        user = models.User(person, "password")
        company = models.Company(address_c, user, "gsm", "phone", "mail", "tva_number", "iban", "bic", "name")
        self.db.add_company(company)
        self.assertEqual(self.db.get_address(), [(1, 'street_c', 'number_c', 'postal_code_c', 'city_c'), (2, 'street_u', 'number_u', 'postal_code_u', 'city_u')])
        self.assertEqual(self.db.get_person(),
                         [(1, 2, 'last_name', 'first_name', 'gsm', 'mail', 'phone', "12345", 'remark')])
        self.assertEqual(self.db.get_company(), [(1, 1, 1, "gsm", "phone", "mail", "tva_number", "iban", "bic", "name")])
        company.address.postal_code = "test_CP_company"
        self.db.update_company(company)
        company.address.street = "test_street_company"
        self.db.update_company(company)
        self.assertEqual(company.address.street, "test_street_company")
        sol = [(1, 'test_street_company', 'number_c', 'test_CP_company', 'city_c'), (2, 'street_u', 'number_u', 'postal_code_u', 'city_u')]
        tmp = self.db.get_address()
        for i in range(len(tmp)):
            for j in range(len(tmp[i])):
                self.assertEqual(tmp[i][j], sol[i][j])

        self.db.remove_company(company)
        self.assertEqual(self.db.get_address(), [])
        self.assertEqual(self.db.get_person(), [])
        self.assertEqual(self.db.get_user(), [])
        self.assertEqual(self.db.get_company(), [])


if __name__ == '__main__':
    unittest.main()
