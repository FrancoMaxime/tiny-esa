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
                     phone text NOT  NULL, remark text NOT NULL,
                     FOREIGN KEY(address_id) REFERENCES address(address_id))''')
                     
        self.c.execute('''CREATE TABLE company (address_id INTEGER NOT NULL, user_id INTEGER NOT NULL,
                    gsm text NOT NULL, phone text NOT NULL, mail text NOT NULL, tva_number text NOT NULL,
                    iban text NOT NULL, bic text NOT NULL, name text NOT NULL,
                    FOREIGN KEY(address_id) REFERENCES address(address_id),
                    FOREIGN KEY(user_id) REFERENCES user(user_id))''')
                    
        self.c.execute('''CREATE TABLE user (user_id INTEGER PRIMARY KEY autoincrement, person_id INTEGER NOT NULL,
                     timestamp text NOT NULL, password text NOT NULL,
                     FOREIGN KEY(person_id) REFERENCES person(person_id))''')
                     
        self.c.execute('''CREATE TABLE customer (customer_id INTEGER PRIMARY KEY autoincrement,
                     person_id INTEGER NOT NULL, timestamp text NOT NULL, evalutation text NOT NULL,
                     FOREIGN KEY(person_id) REFERENCES person(person_id))''')
                     
        self.c.execute('''CREATE TABLE bill(bill_id INTEGER PRIMARY KEY autoincrement, customer_id INTEGER NOT NULL,
                      user_id INTEGER NOT NULL, num_ref text NOT NULL, billing_date text NOT NULL,
                      due_date text NOT NULL, tva_rate INTEGER NOT NULL, paid text NOT NULL, invoiced text NOT NULL,
                     FOREIGN KEY(user_id) REFERENCES user(user_id), FOREIGN KEY(customer_id) 
                     REFERENCES customer(customer_id))''')
                     
        self.c.execute('''CREATE TABLE product(bill_id, description text NOT NULL, amount INTEGER NOT NULL,
                      price_HT REAL NOT NULL, FOREIGN KEY(bill_id) REFERENCES bill(bill_id))''')
        self.conn.commit()
        
    def get_object(self, table_name, row, condition):
        if condition is not None:
            self.c.execute("SELECT " + row + " FROM " + table_name + " where " + condition)
            return self.c.fetchall()

        self.c.execute("SELECT " + row + " FROM " + table_name)
        return self.c.fetchall()

    def add_address(self, address):
        self.c.execute("INSERT INTO address(street, number, postal_code,city) VALUES("+address.__str__()+")")
        self.conn.commit()
        address.id = int(self.get_address(row = 'max(address_id)')[0][0])

    def get_address(self, row='*', condition=None):
        return self.get_object("address", row, condition)

    def update_address(self,address):
        if address.get_id() > 0:
            self.c.execute("UPDATE address SET street = '" + address.get_street()+"', number = '" +
                           address.get_number() + "', postal_code = '" + address.get_postal_code() + "', city = '" +
                           address.get_city() + "' WHERE address_id = " + str(address.get_id()))
            self.conn.commit()
        else:
            print("ERROOOOOR update address sans ID")
        
    def remove_address(self, address):
        if address.get_id() > 0:
            self.c.execute("DELETE FROM address WHERE address_id = " + str(address.get_id()))
            self.conn.commit()
        else:
            print("ERROOOOOR remove address sans ID")

    def add_person(self, person):
        if person.get_address().get_id() < 0:
            self.add_address(person.get_address())

        self.c.execute("INSERT INTO person(address_id, last_name, first_name, gsm, phone, mail, remark) VALUES(" +
                       person.__str__() + ")")
        self.conn.commit()
        person.id = int(self.get_person(row='max(person_id)')[0][0])

    def remove_person(self, person):
        if person.get_id() > 0:
            self.c.execute("DELETE FROM person WHERE person_id = " + str(person.get_id()))
            self.conn.commit()
            self.remove_address(person.get_address())
        else:
            print("EROOOR remove person")

    def get_person(self, row="*", condition=None):
        return self.get_object("person", row, condition)

    def update_person(self, person):
        if person.get_id() > 0:
            self.update_address(person.get_address())
            self.c.execute("UPDATE person SET first_name = '" + person.get_first_name()+"', last_name = '" +
                           person.get_last_name() + "', gsm = '" + person.get_gsm() + "', phone = '" +
                           person.get_phone() + "', mail = '" + person.get_mail() + "', remark = '" +
                           person.get_remark() + "' WHERE person_id = " + str(person.get_id()))
            self.conn.commit()

        else:
            print("ERROOOOOR update person sans ID")

    def add_user(self, user):
        if user.get_person().get_id() < 0:
            self.add_person(user.get_person())
        self.c.execute("INSERT INTO user(person_id, timestamp, password) VALUES("+user.__str__()+")")
        self.conn.commit()
        user.id = int(self.get_user(row='max(user_id)')[0][0])

    def get_user(self, row="*", condition = None):
        return self.get_object("user", row, condition)

    def update_user(self, user):
        if user.get_id() > 0:
            self.update_person(user.get_person())
            self.c.execute("UPDATE user SET person_id = '" + str(user.get_person().get_id())+"', timestamp = '" +
                           user.get_timestamp() + "', password = '" + user.get_password() +
                           "' WHERE user_id = " + str(user.get_id()))
            self.conn.commit()
        else:
            print("ERROOOOOR update user sans ID")

    def remove_user(self,user):
        if user.get_id() > 0:
            self.c.execute("DELETE FROM user WHERE user_id = " + str(user.get_id()))
            self.conn.commit()
            self.remove_person(user.get_person())
        else:
            print("EROOOR remove user")
