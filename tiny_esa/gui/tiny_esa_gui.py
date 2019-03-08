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
import datetime
import os
from tiny_esa.pdf import pdf_generation
from tiny_esa.models import models
from tiny_esa.utils import utils_time
from tiny_esa.db_handler import db_handler


LARGE_FONT = ("Verdana", 12)


class TinyESA(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default='tiny_esa/pictures/emblem-office.xbm')
        tk.Tk.wm_title(self, "Tiny ESA")
        self.geometry("1600x900")
        self.db_name = "database.db"
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, CreateBill, Credit, CreateUser, CreateCustomer, CreateCompany, InstallingPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        if os.path.isfile(self.db_name):
            self.show_frame(StartPage)
        else:
            self.show_frame(InstallingPage)

        self.db = db_handler.ProjectDatabase(self.db_name)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        cbill = ttk.Button(self, text="Generate a Bill",
                           command=lambda: controller.show_frame(CreateBill))
        cbill.pack()

        cuser = ttk.Button(self, text="Create a new User",
                           command=lambda: controller.show_frame(CreateUser))
        cuser.pack()

        ccustomer = ttk.Button(self, text="Create a new customer",
                               command=lambda: controller.show_frame(CreateCustomer))
        ccustomer.pack()

        credit = ttk.Button(self, text="Credit",
                            command=lambda: controller.show_frame(Credit))
        credit.pack()


class CreateBill(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,padx=10, pady=10)
        self.grid_rowconfigure(50, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.controller = controller

        self.facture_id = tk.StringVar()
        label_facture_id = ttk.Label(self, text="Facture number : ", font=LARGE_FONT)
        label_facture_id.grid(column=0, row=1)
        text_facture_id = ttk.Entry(self, width=12, font=LARGE_FONT, textvariable=self.facture_id)
        text_facture_id.grid(column=1, row=1)

        self.ref_id = tk.StringVar()
        label_ref_id = ttk.Label(self, text="Num/Ref : ", font=LARGE_FONT)
        label_ref_id.grid(column=0, row=2)
        text_ref_id = ttk.Entry(self, width=12, font=LARGE_FONT, textvariable=self.ref_id)
        text_ref_id.grid(column=1, row=2)

        label_tva = ttk.Label(self, text="TVA :", font=LARGE_FONT)
        label_tva.grid(column=0, row=3)
        self.tva_value = tk.DoubleVar()
        radio_tva1 = ttk.Radiobutton(self, width=12, text='6%', value=0.06, variable=self.tva_value)
        radio_tva1.grid(column=1, row=3)
        radio_tva2 = ttk.Radiobutton(self, width=12, text='12%', value=0.12, variable=self.tva_value)
        radio_tva2.grid(column=2, row=3)
        radio_tva3 = ttk.Radiobutton(self, width=12, text='21%', value=0.21, variable=self.tva_value)
        radio_tva3.grid(column=3, row=3)

        self.date_fact = tk.StringVar()
        self.date_fact.set(str(datetime.datetime.now()).split(' ')[0])
        label_date_fact = ttk.Label(self, text="Date Facturation : ", font=LARGE_FONT)
        label_date_fact.grid(column=0, row=4)
        text_date_fact = ttk.Entry(self, width=12, font=LARGE_FONT, textvariable=self.date_fact)
        text_date_fact.grid(column=1, row=4)

        self.date_echeance = tk.StringVar()
        self.date_echeance.set(str(datetime.datetime.now()).split(' ')[0])
        label_date_echeance = ttk.Label(self, text="Date Echeance : ", font=LARGE_FONT)
        label_date_echeance.grid(column=0, row=5)
        text_date_echeance = ttk.Entry(self, width=12, font=LARGE_FONT, textvariable=self.date_echeance)
        text_date_echeance.grid(column=1, row=5)

        self.r = 7
        self.tested = []
        self.elements = []
        label_description = ttk.Label(self, text="Description", width=60, font=LARGE_FONT)
        label_description.grid(column=0, row=self.r - 1)
        label_quantite = ttk.Label(self, text="Quantite", width=20, font=LARGE_FONT)
        label_quantite.grid(column=1, row=self.r - 1)
        label_puht = ttk.Label(self, text="PU HT", width=20, font=LARGE_FONT)
        label_puht.grid(column=2, row=self.r - 1)
        label_totalht = ttk.Label(self, text="Total HT EUR", width=20, font=LARGE_FONT)
        label_totalht.grid(column=3, row=self.r - 1)
        self.clicked()
        btn = ttk.Button(self, text="Ajouter un element", command=self.clicked)

        btn.grid(column=5, row=4)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(column=0, row=49)

        button2 = ttk.Button(self, text="Credits",
                             command=lambda: controller.show_frame(Credit))
        button2.grid(column=1, row=49)
        button3 = ttk.Button(self, text="Generer la facture", command=self.generate)
        button3.grid(column=2, row=49)

    def clicked(self):
        self.tested.append([])
        self.elements.append([])
        self.elements[-1].append(tk.StringVar())
        self.elements[-1].append(tk.StringVar())
        self.elements[-1].append(tk.StringVar())
        self.elements[-1].append(tk.StringVar())

        self.tested[-1].append(ttk.Entry(self, width=60, font=LARGE_FONT, textvariable=self.elements[-1][0]))
        self.tested[-1][0].grid(column=0, row=self.r)

        self.tested[-1].append(ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.elements[-1][1]))
        self.tested[-1][1].grid(column=1, row=self.r)

        self.tested[-1].append(ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.elements[-1][2]))
        self.tested[-1][2].grid(column=2, row=self.r)

        self.tested[-1].append(ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.elements[-1][3]))
        self.tested[-1][3].grid(column=3, row=self.r)
        self.r += 1

    def generate(self):
        print("generate")


class Credit(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="CreateBill",
                             command=lambda: controller.show_frame(CreateBill))
        button2.pack()


class CreateUser(tk.Frame):
    def __init__(self, parent, controller, embedded=False):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.grid_rowconfigure(50, weight=1)
        self.grid_columnconfigure(10, weight=1)
        self.controller = controller
        label = ttk.Label(self, text="Creation of a new user", font=LARGE_FONT)
        label.grid(column=1, row=1, pady=5)

        self.person = CreatePerson(self)
        self.person.grid(column=1, row=1, columnspan=9)

        self.password = tk.StringVar()
        label_password = ttk.Label(self, text="Mot de passe : ", font=LARGE_FONT)
        label_password.grid(column=1, row=2, padx=10, pady=5)
        text_password = ttk.Entry(self, width=30, font=LARGE_FONT, textvariable=self.password, show="*")
        text_password.grid(column=2, row=2, pady=5)
        if not embedded:
            button3 = ttk.Button(self, text="Creer le nouvel utilisateur", command=self.generate_user)
            button3.grid(column=9, row=49)

    def generate_user(self):
        person = self.person.generate_person()
        user = models.User(person, self.password.get())
        self.controller.db.add_user(user)
        return user


class CreateCustomer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.grid_rowconfigure(50, weight=1)
        self.grid_columnconfigure(10, weight=1)
        self.controller = controller
        label = ttk.Label(self, text="Creation of a new customer", font=LARGE_FONT)
        label.grid(column=1, row=1, columnspan=10, pady=5)

        self.person = CreatePerson(self)
        self.person.grid(column=1, row=1, columnspan=9)

        self.evaluation = tk.StringVar()
        label_evaluation = ttk.Label(self, text="Evaluation : ", font=LARGE_FONT)
        label_evaluation.grid(column=1, row=2, padx=10, pady=5)
        text_evaluation = ttk.Entry(self, width=50, font=LARGE_FONT, textvariable=self.evaluation)
        text_evaluation.grid(column=2, row=2, pady=5)

        button3 = ttk.Button(self, text="Creer le nouveau client", command=self.generate_customer)
        button3.grid(column=9, row=49)

    def generate_customer(self):
        person = self.person.generate_person()
        customer = models.Customer(person, self.evaluation.get())
        return customer


class CreateAddress(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.grid_rowconfigure(50, weight=1)
        self.grid_columnconfigure(10, weight=1)

        self.street = tk.StringVar()
        label_street = ttk.Label(self, text="Rue : ", font=LARGE_FONT)
        label_street.grid(column=1, row=1, pady=5)
        text_street = ttk.Entry(self, width=80, font=LARGE_FONT, textvariable=self.street)
        text_street.grid(column=2, columnspan=4, row=1, pady=5)

        self.number = tk.StringVar()
        label_number = ttk.Label(self, text="N° : ", font=LARGE_FONT)
        label_number.grid(column=6, row=1, padx=10, pady=5)
        text_number = ttk.Entry(self, width=8, font=LARGE_FONT, textvariable=self.number)
        text_number.grid(column=7, row=1, pady=5)

        self.postal_code = tk.StringVar()
        label_postal_code = ttk.Label(self, text="Code postal : ", font=LARGE_FONT)
        label_postal_code.grid(column=1, row=2, pady=5)
        text_postal_code = ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.postal_code)
        text_postal_code.grid(column=2, row=2, pady=5)

        self.city = tk.StringVar()
        label_city = ttk.Label(self, text="City : ", font=LARGE_FONT)
        label_city.grid(column=3, row=2, padx=10, pady=5)
        text_city = ttk.Entry(self, width=30, font=LARGE_FONT, textvariable=self.city)
        text_city.grid(column=4, row=2, pady=5)

    def generate_address(self):
        address = models.Address(self.street.get(), self.number.get(), self.postal_code.get(), self.city.get())
        return address


class CreatePerson(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.grid_rowconfigure(50, weight=1)
        self.grid_columnconfigure(10, weight=1)

        self.lastname = tk.StringVar()
        label_lastname = ttk.Label(self, text="Nom : ", font=LARGE_FONT)
        label_lastname.grid(column=1, row=2, pady=5)
        text_lastname = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.lastname)
        text_lastname.grid(column=2, row=2, pady=5)

        self.firstname = tk.StringVar()
        label_firstname = ttk.Label(self, text="Prénom : ", font=LARGE_FONT)
        label_firstname.grid(column=1, row=3, pady=5)
        text_firstname = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.firstname)
        text_firstname.grid(column=2, row=3, pady=5)

        self.address_frame = CreateAddress(self)
        self.address_frame.grid(column=1, row=4, rowspan=3, columnspan=5)

        self.gsm = tk.StringVar()
        label_gsm = ttk.Label(self, text="GSM : ", font=LARGE_FONT)
        label_gsm.grid(column=1, row=7, pady=5)
        text_gsm = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.gsm)
        text_gsm.grid(column=2, row=7, pady=5)

        self.phone = tk.StringVar()
        label_phone = ttk.Label(self, text="Téléphone fixe : ", font=LARGE_FONT)
        label_phone.grid(column=1, row=8, pady=5)
        text_phone = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.phone)
        text_phone.grid(column=2, row=8, pady=5)

        self.mail = tk.StringVar()
        label_mail = ttk.Label(self, text="mail : ", font=LARGE_FONT)
        label_mail.grid(column=1, row=9, pady=5)
        text_mail = ttk.Entry(self, width=50, font=LARGE_FONT, textvariable=self.mail)
        text_mail.grid(column=2, row=9, pady=5)

        self.remark = tk.StringVar()
        label_remark = ttk.Label(self, text="Remark : ", font=LARGE_FONT)
        label_remark.grid(column=1, row=9, pady=5)
        text_remark = ttk.Entry(self, width=100, font=LARGE_FONT, textvariable=self.remark)
        text_remark.grid(column=2, row=9, pady=5)

    def generate_person(self):
        address = self.address_frame.generate_address()
        person = models.Person(address, self.lastname.get(), self.firstname.get(), self.gsm.get(), self.phone.get(),
                               self.mail.get(), utils_time.get_timestamp(), self.remark.get())
        return person


class CreateCompany(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.grid_rowconfigure(50, weight=1)
        self.grid_columnconfigure(10, weight=1)
        self.controller = controller

        label = ttk.Label(self, text="Creation of a Company", font=LARGE_FONT)
        label.grid(column=1, row=0, columnspan=10, pady=5)

        self.name = tk.StringVar()
        label_name = ttk.Label(self, text="Nom entreprise : ", font=LARGE_FONT)
        label_name.grid(column=1, row=1, pady=5)
        text_name = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.name)
        text_name.grid(column=2, row=1, pady=5)

        self.address_frame = CreateAddress(self)
        self.address_frame.grid(column=1, row=2, rowspan=3, columnspan=10)

        self.gsm = tk.StringVar()
        label_gsm = ttk.Label(self, text="GSM entreprise: ", font=LARGE_FONT)
        label_gsm.grid(column=1, row=5, pady=5)
        text_gsm = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.gsm)
        text_gsm.grid(column=2, row=5, pady=5)

        self.phone = tk.StringVar()
        label_phone = ttk.Label(self, text="Fixe entreprise : ", font=LARGE_FONT)
        label_phone.grid(column=1, row=6, pady=5)
        text_phone = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.phone)
        text_phone.grid(column=2, row=6, pady=5)

        self.mail = tk.StringVar()
        label_mail = ttk.Label(self, text="mail : ", font=LARGE_FONT)
        label_mail.grid(column=1, row=7, pady=5)
        text_mail = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.mail)
        text_mail.grid(column=2, row=7, pady=5)

        self.tva_number = tk.StringVar()
        label_tva_number = ttk.Label(self, text="Numero de TVA : ", font=LARGE_FONT)
        label_tva_number.grid(column=1, row=8, pady=5)
        text_tva_number = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.tva_number)
        text_tva_number.grid(column=2, row=8, pady=5)

        self.iban = tk.StringVar()
        label_iban = ttk.Label(self, text="IBAN : ", font=LARGE_FONT)
        label_iban.grid(column=1, row=9, pady=5)
        text_iban = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.iban)
        text_iban.grid(column=2, row=9, pady=5)

        self.bic = tk.StringVar()
        label_bic = ttk.Label(self, text="BIC : ", font=LARGE_FONT)
        label_bic.grid(column=1, row=10, pady=5)
        text_bic = ttk.Entry(self, width=40, font=LARGE_FONT, textvariable=self.bic)
        text_bic.grid(column=2, row=10, pady=5)

    def generate_company(self, user):
        address = self.address_frame.generate_address()
        company = models.Company(address, user, self.gsm.get(), self.phone.get(), self.mail.get(), self.tva_number.get()
                                 , self.iban.get(), self.bic.get(), self.name.get())
        self.controller.db.add_company(company)
        return company


class InstallingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.grid_rowconfigure(50, weight=1)
        self.grid_columnconfigure(10, weight=1)
        self.parent = parent
        self.controller = controller
        label = ttk.Label(self, text="Installing page", font=LARGE_FONT)
        label.grid(column=1, row=0, columnspan=10, pady=5)
        self.state = 0
        self.i_element = CreateUser(self, controller, embedded=True)
        self.i_element.grid(column=1, row=1, rowspan=10, columnspan=10)
        self.user = None

        button3 = ttk.Button(self, text="Etape suivante", command=self.installing)
        button3.grid(column=2, row=49)

    def installing(self):
        if self.state == 0:
            self.user = self.i_element.generate_user()
            self.state += 1
            self.i_element.destroy()
            self.i_element = CreateCompany(self, self.controller)
            self.i_element.grid(column=1, row=1, rowspan=10, columnspan=10)
        elif self.state == 1:
            self.controller.company = self.i_element.generate_company(self.user)

