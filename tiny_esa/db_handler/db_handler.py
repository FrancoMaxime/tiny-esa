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


import sqlite3
import os
from tiny_esa.models import models


class ProjectDatabase(object):
    
    def __init__(self, dbname):
        self.conn = None
        self.c = None
        if os.path.isfile(dbname):
            self.conn = sqlite3.connect(dbname)
            self.c = self.conn.cursor()
        else:
            print("Generation Database file")
            self.conn = sqlite3.connect(dbname)
            self.c = self.conn.cursor()
            self.init_db()
            
    def init_db(self):
        self.c.execute('''CREATE TABLE address
             (address_id INTEGER PRIMARY KEY autoincrement, street text NOT NULL,
             number text NOT NULL, postal_code text NOT NULL, city text NOT  NULL)''')
             
        self.c.execute('''CREATE TABLE person
                     (person_id INTEGER PRIMARY KEY autoincrement, address_id INTEGER NOT NULL,
                     last_name text NOT NULL, first_name text NOT NULL, gsm text NOT  NULL, mail NOT  NULL,
                     phone text NOT  NULL, timestamp text NOT NULL, remark text NOT NULL,
                     FOREIGN KEY(address_id) REFERENCES address(address_id))''')
                     
        self.c.execute('''CREATE TABLE company (company_id INTEGER PRIMARY KEY autoincrement,address_id INTEGER NOT NULL
                    ,user_id INTEGER NOT NULL, gsm text NOT NULL, phone text NOT NULL, mail text NOT NULL,
                    tva_number text NOT NULL, iban text NOT NULL, bic text NOT NULL, name text NOT NULL,
                    FOREIGN KEY(address_id) REFERENCES address(address_id),
                    FOREIGN KEY(user_id) REFERENCES user(user_id))''')
                    
        self.c.execute('''CREATE TABLE user (user_id INTEGER PRIMARY KEY autoincrement, person_id INTEGER NOT NULL,
                     password text NOT NULL,
                     FOREIGN KEY(person_id) REFERENCES person(person_id))''')
                     
        self.c.execute('''CREATE TABLE customer (customer_id INTEGER PRIMARY KEY autoincrement,
                     person_id INTEGER NOT NULL, evaluation text NOT NULL,
                     FOREIGN KEY(person_id) REFERENCES person(person_id))''')
                     
        self.c.execute('''CREATE TABLE bill(bill_id INTEGER PRIMARY KEY autoincrement, customer_id INTEGER NOT NULL,
                      user_id INTEGER NOT NULL, num_ref text NOT NULL, billing_date text NOT NULL,
                      due_date text NOT NULL, tva_rate INTEGER NOT NULL, paid text NOT NULL, invoiced text NOT NULL,
                     FOREIGN KEY(user_id) REFERENCES user(user_id), 
                     FOREIGN KEY(customer_id) REFERENCES customer(customer_id))''')
                     
        self.c.execute('''CREATE TABLE product(product_id INTEGER PRIMARY KEY autoincrement ,bill_id INTEGER NOT NULL, description text NOT NULL, amount INTEGER NOT NULL,
                      price_HT REAL NOT NULL, FOREIGN KEY(bill_id) REFERENCES bill(bill_id))''')
        self.conn.commit()
        
    def get_object(self, table_name, row, join, condition, values):
        if condition is not None and values is not None:
            if join is None:
                self.c.execute("SELECT " + row + " FROM " + table_name + " where " + condition, values)
            else:
                self.c.execute("SELECT " + row + " FROM " + table_name + " " + join + " where " + condition, values)
            return self.c.fetchall()
        if join is None:
            self.c.execute("SELECT " + row + " FROM " + table_name)
        else:
            self.c.execute("SELECT " + row + " FROM " + table_name + " " + join)
        return self.c.fetchall()

    def add_address(self, address):
        if address.id != 0:
            self.c.execute("INSERT INTO address(street, number, postal_code,city) VALUES(" +
                           address.__str__() + ")")
            self.conn.commit()
            address.id = int(self.get_address(row='max(address_id)')[0][0])
        else:
            self.update_address(address)
            print(" Error Add address")

    def get_address(self, row='*', join=None, condition=None, values=None):
        return self.get_object("address", row, join, condition, values)

    def update_address(self, address):
        if address.id > 0:
            self.c.execute("UPDATE address SET street = '" + address.street.replace("'", "''")+"', number = '" +
                           address.number.replace("'", "''") + "', postal_code = '" +
                           address.postal_code.replace("'", "''") + "', city = '" + address.city.replace("'", "''")
                           + "' WHERE address_id = " + str(address.id))
            self.conn.commit()
        else:
            self.add_address(address)
            print("ERROOOOOR update address sans ID")
        
    def remove_address(self, address):
        if address.id > 0:
            self.c.execute("DELETE FROM address WHERE address_id = (?)", (str(address.id), ))
            self.conn.commit()
        else:
            print("ERROOOOOR remove address sans ID")

    def address_db_to_object(self, address_id):
        info = self.get_address(condition="address_id = (?)", values=( str(address_id),))
        tmp = None
        if len(info) > 0:
            tmp = models.Address(info[0][1], info[0][2], info[0][3], info[0][4])
            tmp.id = info[0][0]
        return tmp

    def add_person(self, person):
        if person.address.id < 0:
            self.add_address(person.address)
        if person.id < 0:
            self.c.execute("INSERT INTO person(address_id, last_name, first_name, gsm, phone, mail, timestamp,remark)"
                           + " VALUES(" + person.__str__() + ")")
            self.conn.commit()
            person.id = int(self.get_person(row='max(person_id)')[0][0])
        else:
            self.update_person(person)
            print("ERROR IN ADD PERSON")

    def remove_person(self, person):
        if person.id > 0:
            self.c.execute("DELETE FROM person WHERE person_id = (?)", (str(person.id), ))
            self.conn.commit()
            self.remove_address(person.address)
        else:
            print("EROOOR remove person")

    def get_person(self, row="*", join=None, condition=None, values=None):
        return self.get_object("person", row, join, condition, values)

    def update_person(self, person):
        if person.id > 0:
            self.update_address(person.address)
            self.c.execute("UPDATE person SET first_name = '" + person.first_name.replace("'", "''")
                           + "', last_name = '" + person.last_name.replace("'", "''") + "', gsm = '" +
                           person.gsm.replace("'", "''") + "', phone = '" + person.phone.replace("'", "''") +
                           "', mail = '" + person.mail.replace("'", "''") + "', timestamp ='" + person.timestamp +
                           "', remark = '" + person.remark.replace("'", "''") + "' WHERE person_id = "+ str(person.id))
            self.conn.commit()

        else:
            self.add_person(person)
            print("ERROOOOOR update person sans ID")

    def person_db_to_object(self, person_id):
        info = self.get_person(condition="person_id =(?) ", values=(str(person_id),))
        tmp = None
        if len(info) > 0:
            tmp_address = self.address_db_to_object(info[0][1])
            tmp = models.Person(tmp_address, info[0][2], info[0][3], info[0][4], info[0][6], info[0][5], info[0][7],
                                info[0][8])
            tmp.id = info[0][0]
        return tmp

    def user_db_to_object(self, user_id):
        info = self.get_user(condition="user_id = " + str(user_id))
        tmp = None
        if len(info) > 0:
            tmp_p = self.person_db_to_object(info[0][1])
            if tmp_p is not None:
                tmp = models.User(tmp_p, "tmp")
                tmp.set_password(info[0][2])
                tmp.id = info[0][0]

        return tmp

    def add_user(self, user):
        if user.person.id < 0:
            self.add_person(user.person)
        if user.id < 0:
            self.c.execute("INSERT INTO user(person_id, password) VALUES("+user.__str__() + ")")
            self.conn.commit()
            user.id = int(self.get_user(row='max(user_id)')[0][0])
        else:
            self.update_user(user)
            print("Error add User")

    def get_user(self, row="*", join=None, condition=None, values=None):
        return self.get_object("user", row, join, condition, values)

    def update_user(self, user):
        if user.id > 0:
            self.update_person(user.person)
            self.c.execute("UPDATE user SET person_id = '" + str(user.person.id) + "', password = '"
                           + user.password + "' WHERE user_id = " + str(user.id))
            self.conn.commit()
        else:
            self.add_user(user)
            print("ERROOOOOR update user sans ID")

    def remove_user(self, user):
        if user.id > 0:
            self.c.execute("DELETE FROM user WHERE user_id = (?)", (str(user.id), ))
            self.conn.commit()
            self.remove_person(user.person)
        else:
            print("EROOOR remove user")

    def add_customer(self, customer):
        if customer.person.id < 0:
            self.add_person(customer.person)
        if customer.id < 0:
            self.c.execute("INSERT INTO customer(person_id, evaluation) VALUES(" + customer.__str__() + ")")
            self.conn.commit()
            customer.id = int(self.get_customer(row='max(customer_id)')[0][0])
        else:
            self.update_customer(customer)
            print("Error add Customer")

    def customer_db_to_object(self, customer_id):
        info = self.get_customer(condition="customer_id = (?)", values=(str(customer_id),))
        tmp = None
        if len(info) > 0:
            tmp_p = self.person_db_to_object(info[0][1])
            if tmp_p is not None:
                tmp = models.Customer(tmp_p, info[0][2])
                tmp.id = info[0][0]

        return tmp

    def get_customer(self, row="*", join=None, condition=None, values=None):
        return self.get_object("customer", row, join, condition, values)

    def update_customer(self, customer):
        if customer.id > 0:
            self.update_person(customer.person)
            self.c.execute("UPDATE customer SET person_id = " + str(customer.person.id)
                           + ", evaluation = '" + customer.evaluation.replace("'", "''") +
                           "' WHERE customer_id = " + str(customer.id))
            self.conn.commit()
        else:
            self.add_customer(customer)
            print("ERROOOOOR update customer sans ID")

    def remove_customer(self, customer):
        if customer.id > 0:
            self.c.execute("DELETE FROM customer WHERE customer_id = (?)", (str(customer.id), ))
            self.conn.commit()
            self.remove_person(customer.person)
        else:
            print("EROOOR remove customer")

    def company_db_to_object(self, company_id=1):
        info = self.get_company(condition="company_id = (?)", values=(str(company_id),))
        tmp = None
        if len(info) > 0:
            tmp_u = self.user_db_to_object(info[0][2])
            tmp_a = self.address_db_to_object(info[0][1])
            tmp = models.Company(tmp_a, tmp_u, info[0][3], info[0][4], info[0][5], info[0][6], info[0][7], info[0][8],
                                 info[0][9])
            tmp.id = info[0][0]
        return tmp

    def add_company(self, company):
        if company.id < 0:
            self.add_address(company.address)
        if company.user.id < 0:
            self.add_user(company.user)
        if company.id < 0:
            self.c.execute("INSERT INTO company(address_id, user_id, gsm,phone, mail, tva_number, iban, bic, name) "
                           + "VALUES (" + company.__str__() + ")")
            self.conn.commit()
            company.id = int(self.get_company(row='max(company_id)')[0][0])
        else:
            self.update_company(company)
            print("Error Add company")

    def get_company(self, row="*", join=None, condition=None, values=None):
        return self.get_object("company", row, join, condition, values)

    def update_company(self, company):
        if company.id > 0:
            self.update_address(company.address)
            self.update_user(company.user)
            self.c.execute("UPDATE company SET address_id = " + str(company.address.id) + ", user_id = "
                           + str(company.user.id) + ", gsm = '" + company.gsm.replace("'", "''") + "', phone = '" +
                           company.phone.replace("'", "''") + "', mail = '" + company.mail.replace("'", "''") +
                           "', tva_number = '" + company.tva_number.replace("'", "''") + "', iban = '" +
                           company.iban.replace("'", "''") + "', bic = '" + company.bic.replace("'", "''") +
                           "', name = '" + company.name.replace("'", "''") + "'")
            self.conn.commit()
        else:
            self.add_company(company)
            print("ERROOOOR update company")

    def remove_company(self, company):
        if company.id > 0:
            self.c.execute("DELETE FROM company WHERE company_id = (?)", (str(company.id), ))
            self.conn.commit()
            self.remove_user(company.user)
            self.remove_address(company.address)

        else:
            print("ERROOOR REMOVE company")

    def get_bill(self, row="*", join=None, condition=None, values=None):
        return self.get_object("bill", row, join, condition, values)

    def add_bill(self, bill):
        if bill.id < 0:
            self.add_customer(bill.customer)
            self.add_user(bill.user)
            self.c.execute("INSERT INTO bill(customer_id, user_id, num_ref, billing_date, due_date, tva_rate, paid, " +
                           "invoiced) VALUES (" + bill.__str__() + ")")
            bill.id = int(self.get_bill(row='max(bill_id)')[0][0])
            for product in bill.products.values():
                self.add_product(product)
            self.conn.commit()
        else:
            self.update_bill(bill)

    def bill_db_to_object(self, bill_id):
        info = self.get_bill(condition="bill_id = (?)", values=(str(bill_id),))
        tmp = None
        if len(info) > 0:
            tmp_c = self.customer_db_to_object(info[0][1])
            tmp_u = self.user_db_to_object(info[0][2])
            tmp = models.Bill(tmp_c, tmp_u, info[0][3], info[0][4], info[0][5], info[0][6], info[0][7], info[0][8])
            tmp.id = info[0][0]
            inf = self.get_product(condition="bill_id = " + str(bill_id))
            for i in inf:
                tmp.add_product(self.product_db_to_object(i[0], tmp))
        return tmp

    def update_bill(self, bill):
        if bill.id > 0:
            self.update_customer(bill.customer)
            self.update_user(bill.user)
            self.c.execute("UPDATE bill SET customer_id = " + str(bill.customer.id) + ", user_id = "
                           + str(bill.user.id) + ", num_ref = '" + bill.num_ref.replace("'", "''") +
                           "', billing_date = '" + bill.billing_date.replace("'", "''") + "', due_date = '" +
                           bill.due_date.replace("'", "''") + "', tva_rate = '" + str(bill.tva_rate).replace("'", "''") +
                           "', paid = '" + str(bill.paid) + "', invoiced = '" + str(bill.invoiced) +
                           "' WHERE bill_id = " + str(bill.id))
            for product in bill.products.values():
                self.update_product(product)
            self.conn.commit()
        else:
            self.add_bill(bill)
            print("ERROOOOR update bill")

    def remove_bill(self, bill):
        if bill.id > 0:
            self.c.execute("DELETE FROM bill WHERE bill_id = (?)", (str(bill.id),))
            self.c.execute("DELETE FROM product WHERE bill_id = (?)", (str(bill.id),))
            self.conn.commit()
        else:
            print("ERROOOR REMOVE bill")

    def get_product(self, row="*", join=None, condition=None, values=None):
        return self.get_object("product", row, join, condition, values)

    def add_product(self, product):
        if product.id < 0:
            self.c.execute("INSERT INTO product(bill_id, description, amount, price_ht) VALUES (" +
                           product.__str__() + ")")
            self.conn.commit()
            product.id = int(self.get_product(row='max(product_id)')[0][0])
        else:
            self.update_product(product)

    def update_product(self, product):
        if product.id > 0:
            self.c.execute("UPDATE product SET description = '" + product.description.replace("'", "''")
                           + "', amount = " + str(product.amount) + ", price_ht = " + str(product.price_ht) +
                           " WHERE product_id = " + str(product.id))
            self.conn.commit()
        else:
            self.add_product(product)
            print("ERROOOOOR update product sans ID")

    def remove_product(self, product):
        if product.bill.id > 0:
            self.c.execute("DELETE FROM product WHERE product_id = (?)", (str(product.id),))
            self.conn.commit()
        else:
            print("ERROOOR REMOVE product")

    def product_db_to_object(self, product_id, bill):
        info = self.get_product(condition="product_id = (?)", values=(str(product_id),))
        tmp = None
        if len(info) > 0 and bill.id == info[0][1]:
            tmp = models.Product(bill, info[0][2], info[0][3], info[0][4])
            tmp.id = info[0][0]
        return tmp

