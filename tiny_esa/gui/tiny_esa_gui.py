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
from tiny_esa.pdf import pdf_generation
from tiny_esa.models import models
from tiny_esa.db_handler import db_handler
from tiny_esa.utils import password
from tiny_esa.gui import tiny_esa_embedded


LARGE_FONT = ("Verdana", 12)


class TinyESA(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default='tiny_esa/pictures/emblem-office.xbm')
        tk.Tk.wm_title(self, "Tiny ESA")
        self.geometry("1600x900")
        self.db_name = "database.db"
        self.db = db_handler.ProjectDatabase(self.db_name)
        self.previous = None
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=0)
        container.grid_columnconfigure(0, weight=0)
        self.frames = {}
        self.company = None
        self.user = None
        self.pdf = None

        for F in (StartPage, CreateBill, Credit, CreateUser, CreateCustomer, CreateCompany, InstallingPage, SignIn,
                  CustomerList, UserList, BillList):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=1, sticky="nsew", pady=5)

        if len(self.db.get_user()) == 0 or len(self.db.get_company()) == 0:
            self.show_frame(InstallingPage)
        else:
            self.show_frame(SignIn)
            self.company = self.db.company_db_to_object(1)
        self.menu = MenuLeft(container, self)

    def show_frame(self, cont):
        if self.previous is not None:
            self.previous.reset_frame()
        frame = self.frames[cont]
        frame.tkraise()
        self.previous = frame

    def observer(self, element):
        if element == "user":
            self.frames[UserList].update()
        elif element == "customer":
            self.frames[CustomerList].update()
            self.frames[CreateBill].update()
        elif element == "bill":
            self.frames[BillList].update()
        else:
            print("ERROOOOOR MY UPDATE ON KEY  : " + element)

    def load_element(self, key, element_id):
        if key == "user":
            self.frames[CreateUser].load_user(element_id)
        elif key == "customer":
            self.frames[CreateCustomer].load_customer(element_id)
        elif key == "bill":
            self.frames[CreateBill].load_bill(element_id)
        else:
            print("ERROOOOOR LOAD ELEMENT ON KEY  : " + element_id)

    def show_menu(self):
        self.menu.grid(row=0, column=0, sticky="nsew")


class MenuLeft(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, height=900, padx=10, pady=10, background="blue")
        self.controller = controller
        self.parent = parent
        row = 0
        label = None
        if self.controller.company is not None:
            label = ttk.Label(self, width=20, text=self.controller.company.name, font=LARGE_FONT)
        else:
            label = ttk.Label(self, width=20, text=self.controller.company.name, font=LARGE_FONT)
        label.configure(anchor="center")
        label.grid(column=0, row=row, pady=5)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        row += 1

        cbill = ttk.Button(self, width=20, text="Generate a Bill",
                           command=lambda: controller.show_frame(CreateBill))
        cbill.grid(column=0, row=row, pady=5)
        self.grid_rowconfigure(1, weight=0)
        row += 1

        cuser = ttk.Button(self, width=20, text="Create a new User",
                           command=lambda: controller.show_frame(CreateUser))
        cuser.grid(column=0, row=row, pady=5)
        self.grid_rowconfigure(2, weight=0)
        row += 1

        luser = ttk.Button(self, width=20, text="Consult the users",
                               command=lambda: controller.show_frame(UserList))
        luser.grid(column=0, row=row, pady=5)
        self.grid_rowconfigure(3, weight=0)
        row += 1

        ccustomer = ttk.Button(self, width=20, text="Create a new customer",
                               command=lambda: controller.show_frame(CreateCustomer))
        ccustomer.grid(column=0, row=row, pady=5)
        self.grid_rowconfigure(4, weight=0)
        row += 1

        lcustomer = ttk.Button(self, width=20, text="Consult the customers",
                               command=lambda: controller.show_frame(CustomerList))
        lcustomer.grid(column=0, row=row, pady=5)
        self.grid_rowconfigure(5, weight=0)
        row += 1

        list_bill = ttk.Button(self, width=20, text="Consult the bills",
                               command=lambda: controller.show_frame(BillList))
        list_bill.grid(column=0, row=row, pady=5)
        self.grid_rowconfigure(6, weight=0)
        row += 1

        credit = ttk.Button(self, width=20, text="Credit",
                            command=lambda: controller.show_frame(Credit))
        credit.grid(column=0, row=row, pady=5)
        self.grid_rowconfigure(7, weight=0)
        row += 1
        label = tk.Label(self, width=20, height=900, text="", font=LARGE_FONT, background="blue")
        label.configure(anchor="center")
        label.grid(column=0, row=row, pady=5)

    def reset_frame(self):
        pass


class CreateBill(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.controller = controller
        self.bill = None
        for i in range(50):
            self.grid_rowconfigure(i, weight=0)
        for i in range(10):
            self.grid_columnconfigure(i, weight=0)

        self.client_id = tk.StringVar()
        label_client_id = ttk.Label(self, text="Client : ", font=LARGE_FONT)
        label_client_id.grid(column=0, row=1, pady=5, sticky="NSWE")
        self.lb_facture_id = None
        self.scrollbar = None

        self.error = tk.StringVar()
        self.error_label = ttk.Label(self, textvariable=self.error, font=LARGE_FONT, foreground="red", anchor="center")
        self.error_label.grid(column=0, row=0, columnspan=10, pady=5, sticky="NSWE")


        self.generate_customers()

        self.ref_id = tk.StringVar()
        label_ref_id = ttk.Label(self, text="Num/Ref : ", font=LARGE_FONT)
        label_ref_id.grid(column=0, row=2, sticky="NSWE", pady=5)
        text_ref_id = ttk.Entry(self, width=12, font=LARGE_FONT, textvariable=self.ref_id)
        text_ref_id.grid(column=1, row=2, sticky="NSWE", pady=5)

        label_tva = ttk.Label(self, text="TVA :", font=LARGE_FONT)
        label_tva.grid(column=0, row=3, sticky="NSWE", pady=5)
        self.tva_value = tk.DoubleVar()
        radio_tva1 = ttk.Radiobutton(self, width=12, text='6%', value=0.06, variable=self.tva_value)
        radio_tva1.grid(column=1, row=3, sticky="NSWE", pady=5)
        radio_tva2 = ttk.Radiobutton(self, width=12, text='12%', value=0.12, variable=self.tva_value)
        radio_tva2.grid(column=2, row=3, sticky="NSWE", pady=5)
        radio_tva3 = ttk.Radiobutton(self, width=12, text='21%', value=0.21, variable=self.tva_value)
        radio_tva3.grid(column=3, row=3, sticky="NSWE", pady=5)

        self.date_fact = tk.StringVar()
        self.date_fact.set(str(datetime.datetime.now()).split(' ')[0])
        label_date_fact = ttk.Label(self, text="Date Facturation : ", font=LARGE_FONT)
        label_date_fact.grid(column=0, row=4, sticky="NSWE", pady=5)
        text_date_fact = ttk.Entry(self, width=12, font=LARGE_FONT, textvariable=self.date_fact)
        text_date_fact.grid(column=1, row=4, sticky="NSWE", pady=5)

        self.date_echeance = tk.StringVar()
        self.date_echeance.set(str(datetime.datetime.now()).split(' ')[0])
        label_date_echeance = ttk.Label(self, text="Date Echeance : ", font=LARGE_FONT)
        label_date_echeance.grid(column=0, row=5, sticky="NSWE", pady=5)
        text_date_echeance = ttk.Entry(self, width=12, font=LARGE_FONT, textvariable=self.date_echeance)
        text_date_echeance.grid(column=1, row=5, sticky="NSWE", pady=5)

        self.r = 8
        self.tested = []
        self.elements = []
        label_description = ttk.Label(self, text="Description", width=60, font=LARGE_FONT)
        label_description.grid(column=0, row=self.r - 1, sticky="NSWE")
        label_quantite = ttk.Label(self, text="Quantite", width=20, font=LARGE_FONT)
        label_quantite.grid(column=1, row=self.r - 1, sticky="NSWE")
        label_puht = ttk.Label(self, text="PU HT", width=20, font=LARGE_FONT)
        label_puht.grid(column=2, row=self.r - 1, sticky="NSWE")
        self.clicked()

        btn = ttk.Button(self, text="Ajouter un element", command=self.clicked)
        btn.grid(column=3, row=7, pady=5, sticky="NSWE")

        button3 = ttk.Button(self, text="Generer la facture", command=self.generate_bill)
        button3.grid(column=2, row=49)

    def clicked(self):
        self.tested.append([])
        self.elements.append([])
        self.elements[-1].append(tk.StringVar())
        self.elements[-1].append(tk.StringVar())
        self.elements[-1].append(tk.StringVar())
        self.elements[-1].append(tk.StringVar())

        self.tested[-1].append(ttk.Entry(self, width=60, font=LARGE_FONT, textvariable=self.elements[-1][0]))
        self.tested[-1][0].grid(column=0, row=self.r, sticky="NSWE")

        self.tested[-1].append(ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.elements[-1][1]))
        self.tested[-1][1].grid(column=1, row=self.r, sticky="NSWE")
        self.elements[-1][1].set(0)
        self.elements[-1][2].set(0)
        self.tested[-1].append(ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.elements[-1][2]))
        self.tested[-1][2].grid(column=2, row=self.r, sticky="NSWE")

        self.r += 1

    def generate_bill(self):
        if len(self.lb_facture_id.curselection()) > 0 and self.ref_id.get() is not "":
            customer = self.controller.db.customer_db_to_object(self.lb_facture_id.curselection()[0]+1)
            bill = models.Bill(customer, self.controller.user, self.ref_id.get(), self.date_fact.get(),
                               self.date_echeance.get(), self.tva_value.get())
            error = False
            if self.bill is not None:
                bill.id = self.bill.id
                for k, p in self.bill.products.items():
                    self.controller.db.remove_product(p)
            for e in self.elements:
                if e[0].get() is not "" and float(e[1].get()) > 0 and float(e[2].get()) > 0:
                    p = models.Product(bill, e[0].get(), e[1].get(), e[2].get())
                    bill.add_product(p)
                else:
                    error = True

            if not error:
                self.controller.db.add_bill(bill)
                pdf_generation.TinyPDF.generate(bill, self.controller.company)
                self.controller.observer("bill")
                return self.controller.show_frame(BillList)
        self.error.set("Vous avez fait une erreur en créant la facture.")

    def reset_frame(self):
        self.r = 8
        for i in self.tested:
            for j in i:
                j.destroy()
        self.tested = []
        self.elements = []
        self.clicked()
        self.bill = None

    def update(self):
        self.scrollbar.destroy()
        self.lb_facture_id.destroy()
        self.generate_customers()
        self.r = 8
        self.tested = []
        self.elements = []
        self.clicked()
        self.bill = None

    def generate_customers(self):
        self.lb_facture_id = tk.Listbox(self, width=25, height=4, font=LARGE_FONT)
        self.scrollbar = ttk.Scrollbar(self)

        info = self.controller.db.get_customer()

        for cust in info:
            inf = self.controller.db.get_person(condition="person_id = " + str(cust[1]))
            self.lb_facture_id.insert(cust[0], inf[0][2] + " " + inf[0][3])

        self.lb_facture_id.grid(column=1, row=1, sticky="WE")
        self.scrollbar.grid(column=2, row=1, sticky='wns')
        self.lb_facture_id.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lb_facture_id.yview)

    def load_bill(self, bill_id):
        self.bill = self.controller.db.bill_db_to_object(bill_id)
        print(self.bill)
        self.r = 8
        for i in self.tested:
            for j in i:
                j.destroy()
        self.tested = []
        self.elements = []

        self.lb_facture_id.selection_set(self.bill.customer.id-1)

        self.tva_value.set(float(self.bill.tva_rate))

        self.ref_id.set(self.bill.num_ref)
        self.date_fact.set(self.bill.billing_date)
        self.date_echeance.set(self.bill.due_date)

        for k, v in self.bill.products.items():
            self.tested.append([])
            self.elements.append([])
            self.elements[-1].append(tk.StringVar())
            self.elements[-1].append(tk.StringVar())
            self.elements[-1].append(tk.StringVar())
            self.elements[-1].append(tk.StringVar())

            self.tested[-1].append(ttk.Entry(self, width=60, font=LARGE_FONT, textvariable=self.elements[-1][0]))
            self.tested[-1][0].grid(column=0, row=self.r, sticky="NSWE")

            self.tested[-1].append(ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.elements[-1][1]))
            self.tested[-1][1].grid(column=1, row=self.r, sticky="NSWE")

            self.tested[-1].append(ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.elements[-1][2]))
            self.tested[-1][2].grid(column=2, row=self.r, sticky="NSWE")

            self.tested[-1].append(ttk.Entry(self, width=20, font=LARGE_FONT, textvariable=self.elements[-1][3]))
            self.tested[-1][3].grid(column=3, row=self.r, sticky="NSWE")
            self.r += 1

            self.elements[-1][0].set(v.description)
            self.elements[-1][1].set(v.amount)
            self.elements[-1][2].set(v.price_ht)


class Credit(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_label = ttk.Label(self, text="Tiny ESA", font=LARGE_FONT, anchor="center", width=120)
        title_label.grid(column=0, row=0, sticky='NSWE')
        quote = """\n\nCopyright (C) 2018 Maxime Franco\n\n        
        This program is free software: you can redistribute it and/or modify\n
        it under the terms of the GNU Affero General Public License as\n
        published by the Free Software Foundation, either version 3 of the\n
        License, or (at your option) any later version.\n
        \n
        This program is distributed in the hope that it will be useful,\n
        but WITHOUT ANY WARRANTY; without even the implied warranty of\n
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n
        GNU Affero General Public License for more details.\n
        \n
        You should have received a copy of the GNU Affero General Public License\n
        along with this program.  If not, see <http://www.gnu.org/licenses/>"""
        text1 = tk.Message(self, text=quote)
        text1.grid(column=0, row=3, sticky='NSWE')

    def reset_frame(self):
        pass


class StartPage(tk.Frame):

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

    def reset_frame(self):
        pass


class CreateUser(tk.Frame):
    def __init__(self, parent, controller, embedded=False):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.controller = controller
        self.embedded = embedded
        label = ttk.Label(self, text="Creation of a new user", font=LARGE_FONT, anchor="center")
        label.grid(column=2, row=1, pady=5)
        if not self.embedded:
            self.error = tk.StringVar()
            self.error_label = ttk.Label(self, textvariable=self.error, font=LARGE_FONT, foreground="red")
            self.error_label.grid(column=1, row=2, columnspan=10, pady=5)

        self.person = tiny_esa_embedded.CreatePerson(self)
        self.person.grid(column=1, row=3, columnspan=9)

        self.password = tk.StringVar()
        self.label_password = ttk.Label(self, text="Mot de passe : ", font=LARGE_FONT)
        self.label_password.grid(column=1, row=4, padx=10, pady=5)
        self.text_password = ttk.Entry(self, width=30, font=LARGE_FONT, textvariable=self.password, show="*")
        self.text_password.grid(column=2, row=4, pady=5)
        if not self.embedded:
            button2 = ttk.Button(self, text="Retourner au menu", command=lambda: controller.show_frame(StartPage))
            button2.grid(column=8, row=49)
            button3 = ttk.Button(self, text="Creer le nouvel utilisateur", command=self.generate_user)
            button3.grid(column=9, row=49)
        self.user = None

    def generate_user(self):
        person = self.person.generate_person()
        user = models.User(person, self.password.get())
        if user.is_sanitized() and len(self.password.get()) > 7:
            if self.user is None:
                self.controller.db.add_user(user)
            else:
                user.id = self.user
                self.controller.db.update_user(user)
            print(user.password)
            self.controller.observer("user")
            self.controller.show_frame(UserList)
        elif not self.embedded:
            if len(self.password.get()) < 8:
                self.text_password.configure(foreground="red")
            self.error.set("Erreur, il y a une erreur dans le formulaire. Vérifiez que les champs sont bien remplis")
        if self.embedded:
            return user

    def reset_frame(self):
        self.person.reset_frame()
        self.error.set("")
        self.password.set("")
        self.user = None

    def load_user(self, user_id):
        info = self.controller.db.get_user(condition='user_id == ' + str(user_id))
        self.user = info[0][0]
        self.person.load_person(info[0][1])


class CreateCustomer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, padx=10)
        self.controller = controller
        self.customer = None
        label = ttk.Label(self, text="Creation of a new customer", font=LARGE_FONT)
        label.grid(column=1, row=0)
        for i in range(10):
            self.grid_rowconfigure(i, weight=0)
        for i in range(5):
            self.grid_columnconfigure(i, weight=0)

        self.error = tk.StringVar()
        self.error_label = ttk.Label(self, textvariable=self.error, font=LARGE_FONT, foreground="red")
        self.error_label.grid(column=1, row=1, columnspan=10, pady=5)

        self.person = tiny_esa_embedded.CreatePerson(self)
        self.person.grid(column=0, row=2, columnspan=9, sticky="NSWE")

        self.evaluation = tk.StringVar()
        label_evaluation = ttk.Label(self, width=11, text="Evaluation : ", font=LARGE_FONT)
        label_evaluation.grid(column=0, row=3, pady=5, sticky="NSWE")
        text_evaluation = ttk.Entry(self, width=50, font=LARGE_FONT, textvariable=self.evaluation)
        text_evaluation.grid(column=1, row=3, pady=5, sticky="NSWE")

        button2 = ttk.Button(self, text="Retourner au menu", command=lambda: controller.show_frame(StartPage))
        button2.grid(column=8, row=49)
        button3 = ttk.Button(self, text="Creer le nouveau client", command=self.generate_customer)
        button3.grid(column=9, row=49)

    def generate_customer(self):
        person = self.person.generate_person()
        customer = models.Customer(person, self.evaluation.get())
        if customer is not None and customer.is_sanitized():
            if self.customer is None:
                self.controller.db.add_customer(customer)
            else:
                customer = self.customer
                self.controller.db.update_customer(customer)
            self.controller.observer("customer")
            self.controller.show_frame(CustomerList)
        else:
            self.error.set("Erreur, il y a une erreur dans le formulaire. Vérifiez que les champs sont bien remplis")
        return customer

    def reset_frame(self):
        self.person.reset_frame()
        self.evaluation.set("")
        self.error.set("")
        self.customer = None

    def load_customer(self, customer_id):
        info = self.controller.db.get_customer(condition='customer_id == ' + str(customer_id))
        self.customer = info[0][0]
        self.person.load_person(info[0][1])
        self.evaluation.set(info[0][2])


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

        self.address_frame = tiny_esa_embedded.CreateAddress(self)
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
        if self.state == 0 and self.user is None:
            self.user = self.i_element.generate_user()
            self.state += 1
            self.i_element.destroy()
            self.i_element = CreateCompany(self, self.controller)
            self.i_element.grid(column=1, row=1, rowspan=10, columnspan=10)
        elif self.state == 1:
            self.controller.company = self.i_element.generate_company(self.user)
            self.controller.user = self.user
            self.controller.show_frame(StartPage)
            self.controller.show_menu()

    def reset_frame(self):
        pass


class SignIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.parent = parent
        self.controller = controller
        for i in range(6):
            self.grid_rowconfigure(i, weight=0)
        for i in range(5):
            self.grid_columnconfigure(i, weight=0)

        label = ttk.Label(self, text="Connexion", font=LARGE_FONT, anchor="center")
        label.grid(column=2, row=0, pady=5, sticky="NSWE")

        self.error = tk.StringVar()
        self.errorlabel = ttk.Label(self, textvariable=self.error, font=LARGE_FONT, foreground="red")
        self.errorlabel.grid(column=1, row=2, columnspan=10, pady=5, sticky="NSWE")

        self.mail = tk.StringVar()
        label_mail = ttk.Label(self, text="Mail : ", font=LARGE_FONT)
        label_mail.grid(column=1, row=3, pady=5, sticky="NSWE")
        self.text_mail = ttk.Entry(self, width=50, font=LARGE_FONT, textvariable=self.mail)
        self.text_mail.grid(column=2, row=3, pady=5)

        self.password = tk.StringVar()
        label_password = ttk.Label(self, text="Mot de passe : ", font=LARGE_FONT)
        label_password.grid(column=1, row=4, pady=5, sticky="NSWE")
        self.text_password = ttk.Entry(self, width=50, font=LARGE_FONT, textvariable=self.password, show="*")
        self.text_password.grid(column=2, row=4, pady=5)
        self.grid_rowconfigure(4, weight=0)

        button3 = ttk.Button(self, text="Connexion", command=self.signin)
        button3.grid(column=3, row=5, sticky="NSWE")

    def signin(self):
        person = self.controller.db.get_person(row="*", condition="mail == '" + self.mail.get() + "'")
        config_error = False
        if len(person) > 0:
            user = self.controller.db.get_user(row="*", condition="person_id = " + str(person[0][0]))
            if len(user) > 0 and user[0][2] == password.encrypt(self.password.get(), person[0][7]):
                self.controller.show_menu()
                self.controller.user = self.controller.db.user_db_to_object(user[0][0])
                self.controller.show_frame(StartPage)
            else:
                config_error = True
        else:
            config_error = True

        if config_error:
            self.error.set("Erreur mauvais mot de passe ou mauvais mail!")
            self.text_mail.configure(foreground="red")
            self.text_password.configure(foreground="red")

    def reset_frame(self):
        self.error.set("")
        self.mail.set("")
        self.password.set("")


class CustomerList(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.parent = parent
        self.controller = controller
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.array = None
        self.generate_array()
        button2 = ttk.Button(self, text="Retourner au menu", command=lambda: controller.show_frame(StartPage))
        button2.grid(column=8, row=49)

    def generate_array(self):
        info = self.controller.db.get_customer("customer.customer_id, person.last_name, person.first_name,"
                                               "person.address_id, customer.evaluation",
                                               "INNER JOIN person ON person.person_id = customer.person_id")
        address = "( "
        count = 1
        for i in info:
            self.grid_rowconfigure(count, weight=0)
            address += str(i[3]) + ", "
            count += 1
        if address is not "( ":
            address = address[0: -2]
            address += ")"
            address = self.controller.db.get_address(condition="address_id in " + address)
        else:
            address = "()"
        columns = ["Numero", "Last name", "First name", "Address", "Evaluation"]

        self.array = tiny_esa_embedded.DataArray(self, self.controller, info, columns, address)
        self.array.grid(column=0, row=1, columnspan=25, rowspan=count)

    def update(self):
        self.array.destroy()
        self.generate_array()

    def myupdate(self, customer_id):
        self.controller.load_element("customer", customer_id)
        self.controller.show_frame(CreateCustomer)

    def consult(self, customer_id):
        print(str(customer_id))

    def reset_frame(self):
        pass


class UserList(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.parent = parent
        self.controller = controller
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.array = None
        self.generate_array()
        button2 = ttk.Button(self, text="Retourner au menu", command=lambda: controller.show_frame(StartPage))
        button2.grid(column=8, row=49)

    def update(self):
        self.array.destroy()
        self.generate_array()

    def generate_array(self):
        info = self.controller.db.get_user("user.user_id, person.last_name, person.first_name, person.address_id",
                                           "INNER JOIN person ON person.person_id = user.person_id")
        address = "( "
        count = 1
        for i in info:
            self.grid_rowconfigure(count, weight=0)
            address += str(i[3]) + ", "
            count += 1
        if address is not "( ":
            address = address[0: -2]
            address += ")"
            address = self.controller.db.get_address(condition="address_id in " + address)
        else:
            address = "()"
        columns = ["Numero", "Last name", "First name", "Address"]

        self.array = tiny_esa_embedded.DataArray(self, self.controller, info, columns, address)
        self.array.grid(column=0, row=1, columnspan=25, rowspan=count)

    def myupdate(self, user_id):
        self.controller.load_element("user", user_id)
        self.controller.show_frame(CreateUser)

    def consult(self, user_id):
        print(str(user_id))

    def reset_frame(self):
        pass


class BillList(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.parent = parent
        self.controller = controller
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.array = None
        self.generate_array()
        button2 = ttk.Button(self, text="Retourner au menu", command=lambda: controller.show_frame(StartPage))
        button2.grid(column=8, row=49)

    def update(self):
        print("flip")
        self.array.destroy()
        self.generate_array()

    def generate_array(self):
        info = self.controller.db.get_bill(row="bill.bill_id, person.last_name, person.first_name,"
                                               "p2.last_name, p2.first_name, bill.due_date,"
                                               "bill.invoiced, bill.paid",
                                           join="INNER JOIN user ON bill.user_id = user.user_id INNER JOIN person ON "
                                                "person.person_id = user.person_id INNER JOIN customer ON"
                                                " bill.customer_id = customer.customer_id INNER JOIN person as p2 ON"
                                                " customer.person_id = p2.person_id")

        columns = ["Numero", "User", "Customer", "Due date", "Invoiced", "Paid"]
        inf = []
        for i in info:
            inf.append([i[0], i[2] + " " + i[1], i[4] + " " + i[3], i[5], i[6], i[7]])

        self.array = tiny_esa_embedded.DataArray(self, self.controller, inf, columns)
        self.array.grid(column=0, row=1, columnspan=25, rowspan=len(inf))

    def myupdate(self, bill_id):
        self.controller.load_element("bill", bill_id)
        self.controller.show_frame(CreateBill)

    def consult(self, user_id):
        print(str(user_id))

    def reset_frame(self):
        pass

