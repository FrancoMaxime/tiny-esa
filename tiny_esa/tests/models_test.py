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

from tiny_esa.models import models
from tiny_esa.utils import password as pw


class AddressTestCase(unittest.TestCase):

    def test_creation_address1(self):
        test_address = models.Address("street", "number", "postal_code", "city")

        self.assertEqual(test_address.city, "city")
        self.assertEqual(test_address.number, "number")
        self.assertEqual(test_address.street, "street")
        self.assertEqual(test_address.postal_code, "postal_code")
        self.assertEqual(test_address.id, -1)
        self.assertEqual(test_address.__str__(), "'street', 'number', 'postal_code', 'city'")
        test_address.id = -5
        self.assertEqual(test_address.id, -1)

    def test_creation_address2(self):
        test_address = models.Address("rue d'Angelo", "25A", "cp angelo", "Angelo's city")

        self.assertEqual(test_address.city, "Angelo's city")
        self.assertEqual(test_address.number, "25A")
        self.assertEqual(test_address.street, "rue d'Angelo")
        self.assertEqual(test_address.postal_code, "cp angelo")
        self.assertEqual(test_address.id, -1)
        self.assertEqual(test_address.__str__(), "'rue d''Angelo', '25A', 'cp angelo', 'Angelo''s city'")
        test_address.id = 5
        self.assertEqual(test_address.id, 5)

    def test_update_address(self):
        test_address = models.Address("street", "number", "postal_code", "city")
        test_address.street = "new_street"
        self.assertEqual(test_address.street, "new_street")
        test_address.city = "new_city"
        self.assertEqual(test_address.city, "new_city")
        test_address.number = "new_number"
        self.assertEqual(test_address.number, "new_number")
        test_address.postal_code = "cp"
        self.assertEqual(test_address.postal_code, "cp")

    def test_creation_person(self):
        address = models.Address("street", "number", "postal_code", "city")
        test_person = models.Person(address, "last_name","first_name", "gsm", "phone", "mail", "timestamp", "remark")
        self.assertEqual(test_person.last_name, "last_name")
        self.assertEqual(test_person.first_name, "first_name")
        self.assertEqual(test_person.gsm, "gsm")
        self.assertEqual(test_person.phone, "phone")
        self.assertEqual(test_person.mail, "mail")
        self.assertEqual(test_person.remark, "remark")
        self.assertEqual(test_person.timestamp, "timestamp")
        self.assertEqual(test_person.__str__(), "-1, 'last_name', 'first_name', 'gsm', 'phone', 'mail', 'timestamp',"
                                                " 'remark'")

    def test_update_person(self):
        address = models.Address("street", "number", "postal_code", "city")
        test_person = models.Person(address, "last_name", "first_name", "gsm", "phone", "mail", "timestamp", "remark")
        test_person.last_name = "ln"
        self.assertEqual(test_person.last_name, "ln")
        test_person.first_name = "fn"
        self.assertEqual(test_person.first_name, "fn")
        test_person.gsm = "GSM"
        self.assertEqual(test_person.gsm, "GSM")
        test_person.phone = "PHONE"
        self.assertEqual(test_person.phone, "PHONE")
        test_person.mail = "email"
        self.assertEqual(test_person.mail, "email")
        test_person.remark = "rmk"
        self.assertEqual(test_person.remark, "rmk")

    def test_creation_user(self):
        address = models.Address("street", "number", "postal_code", "city")
        person = models.Person(address, "last_name", "first_name", "gsm", "phone", "mail", "12345", "remark")
        user = models.User(person, "password")
        self.assertEqual(user.password, pw.encrypt("password", user.person.timestamp))
        self.assertTrue(user.compare_password("password"))
        user.password = "Password1"
        self.assertTrue(user.compare_password("Password1"))
        self.assertFalse(user.compare_password("password1"))

    def test_creation_company(self):
        address_u = models.Address("street", "number", "postal_code", "city")
        address_c = models.Address("street", "number", "postal_code", "city")
        person = models.Person(address_u, "last_name", "first_name", "gsm", "phone", "mail", "12345", "remark")
        user = models.User(person, "password")
        company = models.Company(address_c, user, "gsm", "phone", "mail", "tva_number", "iban", "bic", "name")
        self.assertEqual(company.name, "name")
        self.assertEqual(company.bic, "bic")
        self.assertEqual(company.iban, "iban")
        self.assertEqual(company.tva_number, "tva_number")
        self.assertEqual(company.mail, "mail")
        self.assertEqual(company.phone, "phone")
        self.assertEqual(company.gsm, "gsm")

    def test_update_company(self):
        address_u = models.Address("street", "number", "postal_code", "city")
        address_c = models.Address("street", "number", "postal_code", "city")
        person = models.Person(address_u, "last_name", "first_name", "gsm", "phone", "mail", "12345", "remark")
        user = models.User(person, "password")
        company = models.Company(address_c, user, "gsm", "phone", "mail", "tva_number", "iban", "bic", "name")
        company.name = "uname"
        self.assertEqual(company.name, "uname")
        company.bic = "ubic"
        self.assertEqual(company.bic, "ubic")
        company.iban = "uiban"
        self.assertEqual(company.iban, "uiban")
        company.tva_number = "utva"
        self.assertEqual(company.tva_number, "utva")
        company.mail = "umail"
        self.assertEqual(company.mail, "umail")
        company.phone = "uphone"
        self.assertEqual(company.phone, "uphone")
        company.gsm = "ugsm"
        self.assertEqual(company.gsm, "ugsm")
        company.address.street = "test_CP_company"
        self.assertEqual(company.address.street, "test_CP_company")

    def test_create_bill(self):
        address_u = models.Address("street", "number", "postal_code", "city")
        address_c = models.Address("street", "number", "postal_code", "city")
        person_u = models.Person(address_u, "last_name_u", "first_name_u", "gsm_u", "phone_u", "mail_u", "12345", "remark_u")
        person_c = models.Person(address_c, "last_name_c", "first_name_c", "gsm_c", "phone_c", "mail_c", "12345", "remark_c")
        user = models.User(person_u, "password")
        customer = models.Customer(person_c, "evaluation")
        bill = models.Bill(customer, user, "num_ref", "billing_date", "due_date", "tva_rate")
        self.assertEqual(bill.customer.evaluation, "evaluation")
        self.assertEqual(bill.num_ref, "num_ref")
        self.assertEqual(bill.billing_date, "billing_date")
        self.assertEqual(bill.due_date, "due_date")
        self.assertEqual(bill.tva_rate, "tva_rate")
        self.assertEqual(bill.paid, False)
        self.assertEqual(bill.invoiced, False)
        self.assertTrue(bill.user.compare_password("password"))

    def test_update_bill(self):
        address_u = models.Address("street", "number", "postal_code", "city")
        address_c = models.Address("street", "number", "postal_code", "city")
        person_u = models.Person(address_u, "last_name_u", "first_name_u", "gsm_u", "phone_u", "mail_u", "12345",
                                 "remark_u")
        person_c = models.Person(address_c, "last_name_c", "first_name_c", "gsm_c", "phone_c", "mail_c", "12345",
                                 "remark_c")
        user = models.User(person_u, "password")
        customer = models.Customer(person_c, "evaluation")
        bill = models.Bill(customer, user, "num_ref", "billing_date", "due_date", "tva_rate")
        bill.customer.evaluation = "eval"
        self.assertEqual(bill.customer.evaluation, "eval")
        bill.num_ref = "N/R"
        self.assertEqual(bill.num_ref, "N/R")
        bill.billing_date = "BD"
        self.assertEqual(bill.billing_date, "BD")
        bill.due_date = "DD"
        self.assertEqual(bill.due_date, "DD")
        bill.tva_rate = "TR"
        self.assertEqual(bill.tva_rate, "TR")
        bill.paid = True
        self.assertEqual(bill.paid, True)
        bill.invoiced = True
        self.assertEqual(bill.invoiced, True)
        self.assertTrue(bill.user.compare_password("password"))


if __name__ == '__main__':
    unittest.main()
