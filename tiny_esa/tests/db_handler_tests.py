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

    def test_db_bill(self):
        address_u = models.Address("street", "number", "postal_code", "city")
        address_c = models.Address("street", "number", "postal_code", "city")
        person_u = models.Person(address_u, "last_name_u", "first_name_u", "gsm_u", "phone_u", "mail_u", "12345",
                                 "remark_u")
        person_c = models.Person(address_c, "last_name_c", "first_name_c", "gsm_c", "phone_c", "mail_c", "12345",
                                 "remark_c")
        user = models.User(person_u, "password")
        customer = models.Customer(person_c, "evaluation")
        bill = models.Bill(customer, user, "num_ref", "billing_date", "due_date", "tva_rate")
        self.db.add_bill(bill)
        for i in range(5):
            p = models.Product(bill, "description_"+str(i), i+1, 50.00)
            self.db.add_product(p)
            bill.add_product(p)
        sol = [(1, 1, 1, 'num_ref', 'billing_date', 'due_date', 'tva_rate', 'False', 'False')]
        tmp = self.db.get_bill()
        for i in range(len(sol[0])):
            self.assertEqual(tmp[0][i], sol[0][i])
        sol = [(1, 1, 'description_0', 1, 50.0),
               (2, 1, 'description_1', 2, 50.0),
               (3, 1, 'description_2', 3, 50.0),
               (4, 1, 'description_3', 4, 50.0),
               (5, 1, 'description_4', 5, 50.0)]
        tmp = self.db.get_product()

        for i in range(len(tmp)):
            for j in range(len(tmp[i])):
                self.assertEqual(tmp[i][j], sol[i][j])
        bill.num_ref = "N/R"
        bill.due_date = "DD"
        bill.invoiced = True
        bill.products[4].description = "TEST MOD DESCRIPTION"
        self.db.update_bill(bill)
        sol = [(1, 1, 1, 'N/R', 'billing_date', 'DD', 'tva_rate', 'False', 'True')]
        tmp = self.db.get_bill()
        for i in range(len(sol[0])):
            self.assertEqual(tmp[0][i], sol[0][i])

        sol = [(1, 1, 'description_0', 1, 50.0),
               (2, 1, 'description_1', 2, 50.0),
               (3, 1, 'description_2', 3, 50.0),
               (4, 1, "TEST MOD DESCRIPTION", 4, 50.0),
               (5, 1, 'description_4', 5, 50.0)]
        tmp = self.db.get_product()
        for i in range(len(tmp)):
            for j in range(len(tmp[i])):
                self.assertEqual(tmp[i][j], sol[i][j])

        self.db.remove_bill(bill)
        self.assertEqual(self.db.get_bill(), [])
        self.assertEqual(self.db.get_product(), [])


if __name__ == '__main__':
    unittest.main()
