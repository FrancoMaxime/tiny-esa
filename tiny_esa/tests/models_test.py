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

    def test_creation_address(self):
        test_address = models.Address("street", "number", "postal_code", "city")
        self.assertEqual(test_address.get_city(), "city")
        self.assertEqual(test_address.get_number(), "number")
        self.assertEqual(test_address.get_street(), "street")
        self.assertEqual(test_address.get_postal_code(), "postal_code")
        self.assertEqual(test_address.__str__(), "'street', 'number', 'postal_code', 'city'")

    def test_update_address(self):
        test_address = models.Address("street", "number", "postal_code", "city")
        test_address.set_street("new_street")
        self.assertEqual(test_address.get_street(), "new_street")
        test_address.set_city("new_city")
        self.assertEqual(test_address.get_city(), "new_city")
        test_address.set_number("new_number")
        self.assertEqual(test_address.get_number(), "new_number")
        test_address.set_postal_code("cp")
        self.assertEqual(test_address.get_postal_code(), "cp")

    def test_creation_person(self):
        address = models.Address("street", "number", "postal_code", "city")
        test_person = models.Person(address,"last_name","first_name", "gsm", "phone", "mail","timestamp", "remark")
        self.assertEqual(test_person.get_last_name(), "last_name")
        self.assertEqual(test_person.get_first_name(), "first_name")
        self.assertEqual(test_person.get_gsm(), "gsm")
        self.assertEqual(test_person.get_phone(), "phone")
        self.assertEqual(test_person.get_mail(), "mail")
        self.assertEqual(test_person.get_remark(), "remark")
        self.assertEqual(test_person.get_timestamp(), "timestamp")
        self.assertEqual(test_person.__str__(), "-1, 'last_name', 'first_name', 'gsm', 'phone', 'mail', 'timestamp',"
                                                " 'remark'")

    def test_update_person(self):
        address = models.Address("street", "number", "postal_code", "city")
        test_person = models.Person(address, "last_name", "first_name", "gsm", "phone", "mail", "timestamp", "remark")
        test_person.set_last_name("ln")
        self.assertEqual(test_person.get_last_name(), "ln")
        test_person.set_first_name("fn")
        self.assertEqual(test_person.get_first_name(), "fn")
        test_person.set_gsm("GSM")
        self.assertEqual(test_person.get_gsm(), "GSM")
        test_person.set_phone("PHONE")
        self.assertEqual(test_person.get_phone(), "PHONE")
        test_person.set_mail("email")
        self.assertEqual(test_person.get_mail(), "email")
        test_person.set_remark("rmk")
        self.assertEqual(test_person.get_remark(), "rmk")

    def test_creation_user(self):
        address = models.Address("street", "number", "postal_code", "city")
        person = models.Person(address, "last_name", "first_name", "gsm", "phone", "mail", "12345", "remark")
        user = models.User(person,"password")
        self.assertEqual(user.get_password(), pw.encrypt("password", "12345"))
        self.assertTrue(user.compare_password("password"))
        user.set_password("Password1")
        self.assertTrue(user.compare_password("Password1"))
        self.assertFalse(user.compare_password("password1"))


if __name__ == '__main__':
    unittest.main()
