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

from tiny_esa.utils import password as pw


class Address(object):
    def __init__(self, street, number, postal_code, city):
        self.street = street
        self.number = number
        self.postal_code = postal_code
        self.city = city
        self.id = -1
        
    def get_street(self):
        return self.street
        
    def get_number(self):
        return self.number
        
    def get_postal_code(self):
        return self.postal_code
        
    def get_city(self):
        return self.city

    def set_street(self, street):
        self.street = street

    def set_number(self, number):
        self.number = number

    def set_postal_code(self, postal_code):
        self.postal_code = postal_code

    def set_city(self, city):
        self.city = city
        
    def __str__(self):
        return "'"+self.street + "', '" + self.number + "', '" + self.postal_code + "', '" + self.city + "'"
        
    def set_id(self, my_id):
        self.id = my_id
        
    def get_id(self):
        return self.id


class Person(object):
    def __init__(self, address, last_name, first_name, gsm, phone, mail, remark=''):
        self.address = address
        self.last_name = last_name
        self.first_name = first_name
        self.gsm = gsm
        self.phone = phone
        self.mail = mail
        self.remark = remark
        self.id = -1

    def __str__(self):
        return str(self.address.get_id()) + ", '" + self.last_name + "', '" + self.first_name + "', '" +\
               self.gsm + "', '" + self.phone + "', '" + self.mail + "', '" + self.remark + "'"
        
    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def set_id(self, my_id):
        self.id = my_id

    def get_id(self):
        return self.id

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, ln):
        self.last_name = ln

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, fn):
        self.first_name = fn

    def get_gsm(self):
        return self.gsm

    def set_gsm(self, gsm):
        self.gsm = gsm

    def get_phone(self):
        return self.phone

    def set_phone(self, phone):
        self.phone = phone

    def get_mail(self):
        return self.mail

    def set_mail(self, mail):
        self.mail = mail

    def get_remark(self):
        return self.remark

    def set_remark(self, remark):
        self.remark = remark


class User(Person):
    def __init__(self, person, password, timestamp):
        self.person = person
        self.password = pw.encrypt(password, str(timestamp))
        self.timestamp = str(timestamp)
        self.id = -1

    def set_id(self, my_id):
        self.id = my_id

    def get_id(self):
        return self.id

    def get_person(self):
        return self.person

    def set_person(self, person):
        self.person = person

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = pw.encrypt(password, self.timestamp)

    def get_timestamp(self):
        return self.timestamp

    def __str__(self):
        return str(self.person.get_id()) + ", '" + self.timestamp + "', '" + self.password + "'"

    def compare_password(self, password):
        return self.password == pw.encrypt(password, self.timestamp)
