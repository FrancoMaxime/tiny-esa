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


class FrozenClass(object):
    __isfrozen = False

    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError("%r is a frozen class" % self)
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True


class Address(FrozenClass):
    def __init__(self, street, number, postal_code, city):
        self.street = street
        self.number = number
        self.postal_code = postal_code
        self.city = city
        self.id = -1
        self._freeze()
        
    @property
    def street(self):
        return self.__street

    @property
    def number(self):
        return self.__number
        
    @property
    def postal_code(self):
        return self.__postal_code

    @property
    def city(self):
        return self.__city

    @street.setter
    def street(self, value):
        self.__street = value

    @number.setter
    def number(self, value):
        self.__number = value

    @postal_code.setter
    def postal_code(self, value):
        self.__postal_code = value

    @city.setter
    def city(self, value):
        self.__city = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value
        
    def __str__(self):
        return "'" + self.street + "', '" + self.number + "', '" + self.postal_code + "', '" + self.city + "'"


class Person(FrozenClass):
    def __init__(self, address, last_name, first_name, gsm, phone, mail, timestamp, remark=''):
        self.address = address
        self.last_name = last_name
        self.first_name = first_name
        self.gsm = gsm
        self.phone = phone
        self.mail = mail
        self.remark = remark
        self.timestamp = str(timestamp)
        self.id = -1
        self._freeze()

    def __str__(self):
        return str(self.address.id) + ", '" + self.last_name + "', '" + self.first_name + "', '" +\
               self.gsm + "', '" + self.phone + "', '" + self.mail + "', '" + self.timestamp + "', '" + self.remark \
               + "'"
        
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @property
    def gsm(self):
        return self.__gsm

    @gsm.setter
    def gsm(self, value):
        self.__gsm = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value

    @property
    def mail(self):
        return self.__mail

    @mail.setter
    def mail(self, value):
        self.__mail = value

    @property
    def remark(self):
        return self.__remark

    @remark.setter
    def remark(self, value):
        self.__remark = value

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value):
        self.__timestamp = value


class User(FrozenClass):
    def __init__(self, person, pwd):
        self.person = person
        self.password = pwd
        self.id = -1
        self._freeze()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def person(self):
        return self.__person

    @person.setter
    def person(self, value):
        self.__person = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = pw.encrypt(value, self.person.timestamp)

    def __str__(self):
        return str(self.person.id) + ", '" + self.password + "'"

    def compare_password(self, pwd):
        return self.password == pw.encrypt(pwd, self.person.timestamp)


class Customer(FrozenClass):
    def __init__(self, person, evaluation):
        self.person = person
        self.evaluation = evaluation
        self.id = -1
        self._freeze()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def person(self):
        return self.__person

    @person.setter
    def person(self, value):
        self.__person = value

    @property
    def evaluation(self):
        return self.__evaluation

    @evaluation.setter
    def evaluation(self, value):
        self.__evaluation = value

    def __str__(self):
        return str(self.person.id) + ", '" + self.evaluation + "'"


class Company(FrozenClass):
    def __init__(self, address, user, gsm, phone, mail, tva_number, iban, bic, name):
        self.address = address
        self.user = user
        self.gsm = gsm
        self.phone = phone
        self.mail = mail
        self.tva_number = tva_number
        self.iban = iban
        self.bic = bic
        self.name = name
        self.id = -1
        self._freeze()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    def __str__(self):
        return str(self.address.id) + ", " + str(self.user.id) + ", '" + self.gsm + "', '" + self.phone \
               + "', '" + self.mail + "', '" + self.tva_number + "', '" + self.iban + "', '" + self.bic + "', '" \
               + self.name + "'"

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    @property
    def gsm(self):
        return self.__gsm

    @gsm.setter
    def gsm(self, value):
        self.__gsm = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value

    @property
    def mail(self):
        return self.__mail

    @mail.setter
    def mail(self, value):
        self.__mail = value

    @property
    def tva_number(self):
        return self.__tva_number

    @tva_number.setter
    def tva_number(self, value):
        self.__tva_number = value

    @property
    def iban(self):
        return self.__iban

    @iban.setter
    def iban(self, value):
        self.__iban = value

    @property
    def bic(self):
        return self.__bic

    @bic.setter
    def bic(self, value):
        self.__bic = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value


class Bill(object):
    def __init__(self, customer, user, num_ref, billing_date, due_date, tva_rate, paid=False, invoiced=False):
        self.customer = customer
        self.user = user
        self.num_ref = num_ref
        self.billing_date = billing_date
        self.due_date = due_date
        self.tva_rate = tva_rate
        self.paid = paid
        self.invoiced = invoiced
        self.id = -1

    def get_customer(self):
        return self.customer

    def set_customer(self, customer):
        self.customer = customer

    def get_num_ref(self):
        return self.num_ref

    def set_num_ref(self, num_ref):
        self.num_ref = num_ref
