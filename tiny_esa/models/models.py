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

    def __init__(self, id=-1):
        self.id = id

    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError("%r is a frozen class" % self)
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value < 0 and not self.__isfrozen:
            self.__id = value
        elif value > 0:
            self.__id = value
        else:
            print("ERROR SET ID")

    def isfrozen(self):
        return self.__isfrozen

    def is_sanitized(self):
        return self.__id == -1 or self.__id > 0


class Address(FrozenClass):
    def __init__(self, street, number, postal_code, city, id=-1):
        FrozenClass.__init__(self, id)
        self.street = street
        self.number = number
        self.postal_code = postal_code
        self.city = city
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

    @property
    def address(self):
        return self.street + ", " + str(self.number) + ". " + self.postal_code + " " + self.city

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
        
    def __str__(self):
        return "'" + self.street.replace("'", "''")  + "', '" + str(self.number).replace("'", "''")  + "', '" + self.postal_code.replace("'", "''")  + "', '" + self.city.replace("'", "''")  + "'"

    def is_sanitized(self):
        return FrozenClass.is_sanitized(self) and self.street != "" and self.number != "" and self.postal_code != "" and self.city != ""

    @staticmethod
    def address_from_database(data):
        return Address(data[1], data[2], data[3], data[4], data[0])

    def get_full_address(self):
        return self.number + ", " + self.street + "."

    def get_full_city(self):
        return self.postal_code + " " + self.city


class Person(FrozenClass):
    def __init__(self, address, last_name, first_name, gsm, phone, mail, timestamp, remark=''):
        FrozenClass.__init__(self)
        self.address = address
        self.last_name = last_name
        self.first_name = first_name
        self.gsm = gsm
        self.phone = phone
        self.mail = mail
        self.remark = remark
        self.timestamp = str(timestamp)
        self._freeze()

    def __str__(self):
        return str(self.address.id) + ", '" + self.last_name.replace("'", "''")  + "', '" \
               + self.first_name.replace("'", "''")  + "', '" + self.gsm.replace("'", "''") + "', '" +\
               self.phone.replace("'", "''")  + "', '" + self.mail.replace("'", "''") + "', '" +\
               self.timestamp + "', '" + self.remark.replace("'", "''")  + "'"
        
    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

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

    def is_sanitized(self):
        return FrozenClass.is_sanitized(self) and self.address.is_sanitized() and self.last_name != "" \
               and self.first_name != "" and self. mail != "" and self.timestamp != 0 and self.phone != ""\
               and self.gsm != ""

    def get_full_name(self):
        return self.last_name + " " + self.first_name

    def get_bill_info(self):
        tmp = self.get_full_name() + "\n"
        tmp += self.address.get_full_address() + "\n"
        tmp += self.address.get_full_city()
        return tmp


class User(FrozenClass):
    def __init__(self, person, pwd):
        FrozenClass.__init__(self)
        self.person = person
        self.password = pwd
        self._freeze()

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

    @staticmethod
    def data_to_user(data_u, person):
        u = User(person, '')
        u.__password = data_u[2]
        u.id = data_u[0]
        return u

    def is_sanitized(self):
        return FrozenClass.is_sanitized(self) and self.person.is_sanitized() and self.password != ""

    def set_password(self, password):
        self.__password = password


class Customer(FrozenClass):
    def __init__(self, person, evaluation):
        FrozenClass.__init__(self)
        self.person = person
        self.evaluation = evaluation
        self._freeze()

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

    def is_sanitized(self):
        return FrozenClass.is_sanitized(self) and self.person.is_sanitized()


class Company(FrozenClass):
    def __init__(self, address, user, gsm, phone, mail, tva_number, iban, bic, name):
        FrozenClass.__init__(self)
        self.address = address
        self.user = user
        self.gsm = gsm
        self.phone = phone
        self.mail = mail
        self.tva_number = tva_number
        self.iban = iban
        self.bic = bic
        self.name = name
        self._freeze()

    def __str__(self):
        return str(self.address.id) + ", " + str(self.user.id) + ", '" + self.gsm.replace("'", "''") + "', '" + self.phone.replace("'", "''")  \
               + "', '" + self.mail.replace("'", "''") + "', '" + self.tva_number.replace("'", "''") + "', '" + self.iban.replace("'", "''") + "', '" + self.bic.replace("'", "''") + "', '" \
               + self.name.replace("'", "''") + "'"

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

    def is_sanitized(self):
        return FrozenClass.is_sanitized(self) and self.address.is_sanitized() and self.user.is_sanitized() and \
               self.gsm != "" and self.phone != "" and self.bic != "" and self.iban != "" and self.name != "" \
               and self.mail != "" and self.tva_number != ""


class Bill(FrozenClass):
    def __init__(self, customer, user, num_ref, billing_date, due_date, tva_rate, paid=False, invoiced=False):
        FrozenClass.__init__(self)
        self.customer = customer
        self.user = user
        self.num_ref = num_ref
        self.billing_date = billing_date
        self.due_date = due_date
        self.tva_rate = tva_rate
        self.paid = paid
        self.invoiced = invoiced
        self.products = {}
        self._freeze()

    def __str__(self):
        return str(self.customer.id) + ", " + str(self.user.id) + ", '" + str(self.num_ref) + "', '" + self.billing_date \
            + "', '" + self.due_date + "', '" + str(self.tva_rate) + "', '" + str(self.paid) + "', '" + \
            str(self.invoiced) + "'"

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, value):
        self.__customer = value

    @property
    def num_ref(self):
        return self.__num_ref

    @num_ref.setter
    def num_ref(self, value):
        self.__num_ref = value

    @property
    def billing_date(self):
        return self.__billing_date

    @billing_date.setter
    def billing_date(self, value):
        self.__billing_date = value

    @property
    def due_date(self):
        return self.__due_date

    @due_date.setter
    def due_date(self, value):
        self.__due_date = value

    @property
    def tva_rate(self):
        return self.__tva_rate

    @tva_rate.setter
    def tva_rate(self, value):
        self.__tva_rate = value

    @property
    def paid(self):
        return self.__paid

    @paid.setter
    def paid(self, value):
        self.__paid = value

    @property
    def invoiced(self):
        return self.__invoiced

    @invoiced.setter
    def invoiced(self, value):
        self.__invoiced = value

    @property
    def products(self):
        return self.__products

    @products.setter
    def products(self, value):
        self.__products = value

    def add_product(self, p):
        if p.id is not -1:
            self.__products[p.id] = p
        else:
            self.__products[p.description] = p

    def remove_product(self, p):
        self.__products.pop(p.id)

    def is_sanitized(self):
        tmp = True
        for k, v in self.__products.items():
            tmp = tmp and v.is_sanitized()
        return FrozenClass.is_sanitized(self) and self.customer.is_sanitized() and self.user.is_sanitized() \
               and self.num_ref != "" and self. billing_date != "" and self.due_date != "" and self.tva_rate != "" \
               and tmp


class Product(FrozenClass):
    def __init__(self, bill, description, amount, price_ht):
        FrozenClass.__init__(self)
        self.bill = bill
        self.description = description
        self.amount = amount
        self.price_ht = price_ht
        self._freeze()

    def __str__(self):
        return str(self.bill.id) + ",'" + self.description + "', " + str(self.amount) + ", " + str(self.price_ht)

    @property
    def bill(self):
        return self.__bill

    @bill.setter
    def bill(self, value):
        self.__bill = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        self.__amount = value

    @property
    def price_ht(self):
        return self.__price_ht

    @price_ht.setter
    def price_ht(self, value):
        self.__price_ht = value

    def is_sanitized(self):
        return FrozenClass.is_sanitized(self) and self.description != "" and self.amount >= 0 and self.price_ht >= 0.0
