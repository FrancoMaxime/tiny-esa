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
import tkinter as tk
from tkinter import ttk
from tiny_esa.models import models
from tiny_esa.utils import utils_time

LARGE_FONT = ("Verdana", 12)


class DataArray(tk.Frame):
    def __init__(self, parent, controller, infos, columns, address=None):
        tk.Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        ttk.Separator(self, orient="horizontal").grid(row=0, columnspan=2*(len(columns)+2)+1, sticky="NSWE")
        ttk.Separator(self, orient="vertical").grid(column=0, sticky="NSWE")
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.consult_buttons = {}
        self.update_buttons = {}
        self.invoiced_button = {}
        self.paid_button = {}
        self.s = ttk.Style()
        self.s.configure('kim.TButton', background="green")
        self.s.configure('jos.TButton', background="red")
        column = 0
        row = 1
        for c_name in columns:
            self.grid_columnconfigure(column, weight=0)
            ttk.Separator(self, orient="vertical").grid(row=row, column=column, sticky="NSWE")
            column += 1
            if c_name is "Address":
                tmp = ttk.Label(self, text=c_name, font=LARGE_FONT, width=50, anchor="center")
                tmp.grid(column=column, row=row, sticky="NSWE")
            elif c_name in ("Invoiced", "Paid", "Numero"):
                tmp = ttk.Label(self, text=c_name, font=LARGE_FONT, width=7, anchor="center")
                tmp.grid(column=column, row=row, sticky="NSWE")
            elif c_name in ("Customer", "User"):
                tmp = ttk.Label(self, text=c_name, font=LARGE_FONT, width=25, anchor="center")
                tmp.grid(column=column, row=row, sticky="NSWE")
            else:
                tmp = ttk.Label(self, text=c_name, font=LARGE_FONT, width=15, anchor="center")
                tmp.grid(column=column, row=row, sticky="NSWE")
            column += 1
            self.grid_columnconfigure(column, weight=1)
        ttk.Separator(self, orient="vertical").grid(row=row, column=column, sticky="NSWE")
        column += 1
        tmp = ttk.Label(self, text="Action", font=LARGE_FONT, width=20, anchor="center")
        tmp.grid(column=column, row=row, columnspan=3, sticky="NSWE")
        ttk.Separator(self, orient="vertical").grid(row=1, column=column+4, sticky="NSWE")

        row += 1
        ttk.Separator(self, orient="horizontal").grid(row=row, columnspan=2 * (len(columns) + 2) + 1, sticky="NSWE")
        row += 1
        elem_id = 0
        for elem in infos:
            column = 0
            myid = -1
            for data in elem:
                self.grid_columnconfigure(column, weight=0)
                ttk.Separator(self, orient="vertical").grid(row=row, column=2*column, sticky="NSWE")
                if columns[column] is "Address":
                    ad = models.Address.address_from_database(address[elem_id])
                    tmp = ttk.Label(self, text=ad.address, font=LARGE_FONT, width=50, background="white")
                    tmp.grid(column=(2*column)+1, row=row, sticky="NSWE")
                elif columns[column] is columns[0] or columns[column] is "Evaluation":
                    tmp = ttk.Label(self, text=data, font=LARGE_FONT, width=10, anchor="center", background="white")
                    tmp.grid(column=(2*column)+1, row=row, sticky="NSWE")
                    if columns[column] is columns[0]:
                     myid = data
                elif columns[column] in ("Invoiced", "Paid"):
                    color = "jos.TButton"
                    if data == "True":
                        color = "kim.TButton"
                    button = ttk.Button(self, text="modifier", style=color)
                    button.grid(column=(2 * column) + 1, row=row, sticky="NSWE")

                    if columns[column] is "Invoiced":
                        self.invoiced_button[button] = myid
                        button.bind("<Button-1>", self.invoiced_method)
                    else:
                        self.paid_button[button] = myid
                        button.bind("<Button-1>", self.paid_method)

                else:
                    tmp = ttk.Label(self, text=data, font=LARGE_FONT, width=15, background="white")
                    tmp.grid(column=(2*column)+1, row=row, sticky="NSWE")
                column += 1
            self.grid_rowconfigure(row, weight=1)
            ttk.Separator(self, orient="vertical").grid(row=row, column=2 * column, sticky="NSWE")
            button1 = ttk.Button(self, text="modifier")
            button1.grid(column=(2*column)+1, row=row, sticky="NSWE")
            column += 1
            button2 = ttk.Button(self, text="consulter")
            button2.grid(column=(2*column)+1, row=row, sticky="NSWE")
            column += 1
            ttk.Separator(self, orient="vertical").grid(row=row, column=(2 * column)+1, sticky="NSWE")
            row += 1
            ttk.Separator(self, orient="horizontal").grid(row=row, columnspan=2 * (len(columns) + 2) + 1, sticky="NSWE")
            row += 1
            elem_id += 1
            self.update_buttons[button1] = myid
            self.consult_buttons[button2] = myid
            button1.bind("<Button-1>", self.myupdate)
            button2.bind("<Button-1>", self.consult)

    def myupdate(self, event):
        self.parent.myupdate(self.update_buttons[event.widget])

    def consult(self, event):
        self.parent.consult(self.consult_buttons[event.widget])

    def paid_method(self, event):
        self.parent.paid_method(self.paid_button[event.widget])

    def invoiced_method(self, event):
        self.parent.invoiced_method(self.invoiced_button[event.widget])


class CreateAddress(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.address = None
        for i in range(3):
            self.grid_rowconfigure(i, weight=0)
        for i in range(8):
            self.grid_columnconfigure(i, weight=0)

        self.street = tk.StringVar()
        self.label_street = ttk.Label(self, width=15, text="Rue : ", font=LARGE_FONT)
        self.label_street.grid(column=1, row=1, pady=5, sticky="NSWE")
        self.text_street = ttk.Entry(self, width=80, font=LARGE_FONT, textvariable=self.street)
        self.text_street.grid(column=2, columnspan=4, row=1, pady=5, sticky="NSWE")

        self.number = tk.StringVar()
        self.label_number = ttk.Label(self, text="N° : ", font=LARGE_FONT)
        self.label_number.grid(column=6, row=1, padx=10, pady=5, sticky="NSWE")
        self.text_number = ttk.Entry(self, width=8, font=LARGE_FONT, textvariable=self.number)
        self.text_number.grid(column=7, row=1, pady=5, sticky="NSWE")

        self.postal_code = tk.StringVar()
        self.label_postal_code = ttk.Label(self, text="Code postal : ", font=LARGE_FONT)
        self.label_postal_code.grid(column=1, row=2, pady=5, sticky="NSWE")
        self.text_postal_code = ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.postal_code)
        self.text_postal_code.grid(column=2, row=2, pady=5, sticky="NSWE")

        self.city = tk.StringVar()
        self.label_city = ttk.Label(self, text="City : ", font=LARGE_FONT)
        self.label_city.grid(column=3, row=2, padx=10, pady=5, sticky="NSWE")
        self.text_city = ttk.Entry(self, width=30, font=LARGE_FONT, textvariable=self.city)
        self.text_city.grid(column=4, row=2, pady=5, sticky="NSWE")

    def generate_address(self):
        address = models.Address(self.street.get(), self.number.get(), self.postal_code.get(), self.city.get())
        if not address.is_sanitized():
            if self.street.get() == "":
                self.text_street.configure(foreground="red")
            if self.number.get() == "":
                self.text_number.configure(foreground="red")
            if self.postal_code.get() == "":
                self.text_postal_code.configure(foreground="red")
            if self.city.get() == "":
                self.text_city.configure(foreground="red")
        else:
            self.text_street.configure(foreground="black")
            self.text_number.configure(foreground="black")
            self.text_postal_code.configure(foreground="black")
            self.text_city.configure(foreground="black")
        if self.address is not None:
            address.id = self.address
        return address

    def reset_frame(self):
        self.street.set("")
        self.number.set("")
        self.postal_code.set("")
        self.city.set("")
        self.address = None

    def load_address(self, address_id):
        info = self.parent.parent.controller.db.get_address(condition="address_id = " + str(address_id))
        self.address = info[0][0]
        self.street.set(info[0][1])
        self.number.set(info[0][2])
        self.postal_code.set(info[0][3])
        self.city.set(info[0][4])


class CreatePerson(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.person = None
        for i in range(10):
            self.grid_rowconfigure(i, weight=0)
        for i in range(5):
            self.grid_columnconfigure(i, weight=0)

        self.lastname = tk.StringVar()
        self.label_lastname = ttk.Label(self, text="Nom : ", font=LARGE_FONT)
        self.label_lastname.grid(column=1, row=1, pady=5, sticky="NSWE")
        self.text_lastname = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.lastname)
        self.text_lastname.grid(column=2, row=1, pady=5, sticky="NSWE")

        self.firstname = tk.StringVar()
        self.label_firstname = ttk.Label(self, text="Prénom : ", font=LARGE_FONT)
        self.label_firstname.grid(column=1, row=2, pady=5, sticky="NSWE")
        self.text_firstname = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.firstname)
        self.text_firstname.grid(column=2, row=2, pady=5, sticky="NSWE")

        self.address_frame = CreateAddress(self)
        self.address_frame.grid(column=1, row=3, rowspan=3, columnspan=5, pady=5, sticky="NSWE")

        self.gsm = tk.StringVar()
        self.label_gsm = ttk.Label(self, text="GSM : ", font=LARGE_FONT)
        self.label_gsm.grid(column=1, row=6, pady=5, sticky="NSWE")
        self.text_gsm = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.gsm)
        self.text_gsm.grid(column=2, row=6, pady=5, sticky="NSWE")

        self.phone = tk.StringVar()
        self.label_phone = ttk.Label(self, width=10, text="Téléphone fixe : ", font=LARGE_FONT)
        self.label_phone.grid(column=1, row=7, pady=5, sticky="NSWE")
        self.text_phone = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.phone)
        self.text_phone.grid(column=2, row=7, pady=5, sticky="NSWE")

        self.mail = tk.StringVar()
        self.label_mail = ttk.Label(self, text="mail : ", font=LARGE_FONT)
        self.label_mail.grid(column=1, row=8, pady=5, sticky="NSWE")
        self.text_mail = ttk.Entry(self, width=75, font=LARGE_FONT, textvariable=self.mail)
        self.text_mail.grid(column=2, row=8, pady=5, sticky="NSWE")

        self.remark = tk.StringVar()
        self.label_remark = ttk.Label(self, text="Remark : ", font=LARGE_FONT)
        self.label_remark.grid(column=1, row=9, pady=5, sticky="NSWE")
        self.text_remark = ttk.Entry(self, width=75, font=LARGE_FONT, textvariable=self.remark)
        self.text_remark.grid(column=2, row=9, pady=5, sticky="NSWE")

    def generate_person(self):
        address = self.address_frame.generate_address()
        person = models.Person(address, self.lastname.get(), self.firstname.get(), self.gsm.get(), self.phone.get(),
                               self.mail.get(), utils_time.get_timestamp(), self.remark.get())
        if not person.is_sanitized():
            if self.lastname.get() == "":
                self.text_lastname.configure(foreground="red")
            if self.firstname.get() == "":
                self.text_firstname.configure(foreground="red")
            if self.gsm.get() == "":
                self.text_gsm.configure(foreground="red")
            if self.phone.get() == "":
                self.text_phone.configure(foreground="red")
            if self.mail.get() == "":
                self.text_mail.configure(foreground="red")
        else:
            self.text_lastname.configure(foreground="black")
            self.text_firstname.configure(foreground="black")
            self.text_gsm.configure(foreground="black")
            self.text_phone.configure(foreground="black")
            self.text_mail.configure(foreground="black")
        if self.person is not None:
            print(str(person.timestamp))
            person.id = self.person[0][0]
            person.timestamp = self.person[0][7]
            print(str(person.timestamp))
        return person

    def reset_frame(self):
        self.lastname.set("")
        self.firstname.set("")
        self.gsm.set("")
        self.phone.set("")
        self.mail.set("")
        self.remark.set("")
        self.person = None
        self.address_frame.reset_frame()

    def load_person(self, person_id):
        info = self.parent.controller.db.get_person(condition="person_id = " + str(person_id))
        self.person = info
        self.lastname.set(info[0][2])
        self.firstname.set(info[0][3])
        self.gsm.set(info[0][4])
        self.phone.set(info[0][6])
        self.mail.set(info[0][5])
        self.remark.set(info[0][8])
        self.address_frame.load_address(info[0][1])


