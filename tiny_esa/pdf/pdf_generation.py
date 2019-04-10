#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name of the project
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

from fpdf import FPDF


class TinyPDF(FPDF):

    def __init__(self, company):
        FPDF.__init__(self)
        self.company = company

    def header(self):
        # Set up a logo
        self.image('tiny_esa/pictures/lnsc.png', 20, 8, 60)
        self.set_font('Times_New_Roman', "", 9)
        self.set_text_color(31, 59, 115)
        # Add an address
        self.cell(100)
        self.cell(45, 5, self.company.address.get_full_address(), ln=0)
        self.cell(45, 5, 'GSM :' + self.company.gsm, ln=1)
        self.cell(100)
        self.cell(45, 5, self.company.address.get_full_city(), ln=0)
        self.cell(45, 5, 'Tél : ' + self.company.phone, ln=1)
        self.cell(145)
        self.cell(45, 5, 'Email : ' + self.company.mail, ln=1)
        
        # Line break
        self.ln(20)
 
    def footer(self):
        self.set_y(-17)
        self.set_font('Times_New_Roman', "", 9)
        self.set_text_color(31, 59, 115)
        self.set_draw_color(31, 59, 115)
        self.line(30, 275, 180, 275)
        self.cell(25)
        self.cell(50, 5, 'TVA: ' + self.company.tva_number, ln=0)
        self.cell(60, 5, 'IBAN: ' + self.company.iban, ln=0)
        self.cell(50, 5, 'BIC: ' + self.company.bic, ln=1)

    @staticmethod
    def generate(bill, company):
        bd = "LTRB"
        pdf = TinyPDF(company)
        pdf.add_font('Times_New_Roman', '', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf', uni=True)
        pdf.add_font('Times_New_RomanB', 'B', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.ttf',
                     uni=True)
        pdf.set_font('Times_New_RomanB', "B", 20)
        pdf.set_title("Facture")
        pdf.set_author(bill.user.person.get_full_name())
        pdf.add_page()
        
        pdf.set_font('Times_New_RomanB', "B", 20)
        pdf.cell(10)
        pdf.cell(100, 20, 'FACTURE', ln=0)
        pdf.set_line_width(0.5)

        pdf.set_font('Times_New_Roman', "", 11)
        pdf.multi_cell(70, 11, txt=bill.customer.person.get_bill_info(), border=bd, align="C")
        
        pdf.set_line_width(0.4)
        pdf.set_font('Times_New_RomanB', "B", 12)
        pdf.cell(10)
        pdf.cell(100, 20, 'N/REF : ' + str(bill.num_ref), ln=1)
        
        pdf.set_font('Times_New_Roman', "", 11)
        pdf.cell(10)
        pdf.cell(60, 12, 'Date de facturation', ln=0, border=bd, align="C")
        pdf.cell(60, 12, 'Echéance', ln=1, border=bd, align="C")
        pdf.cell(10)
        pdf.cell(60, 10, str(bill.billing_date), ln=0, border=bd, align="C")
        pdf.cell(60, 10, str(bill.due_date), ln=1, border=bd, align="C")
        
        pdf.cell(10, 5, '', ln=1)
        pdf.cell(10)
        pdf.set_fill_color(192, 192, 192)
        pdf.cell(80, 12, 'Description', ln=0, border=bd, align="C", fill=True)
        pdf.cell(30, 12, 'Quantité', ln=0, border=bd, align="C", fill=True)
        pdf.cell(30, 12, 'PU HT', ln=0, border=bd, align="C", fill=True)
        pdf.cell(30, 12, 'Total HT EUR', ln=1, border=bd, align="C", fill=True)
        total_ht = 0
        for k,p in bill.products.items():
            tmp_prix = float(p.price_ht)
            tmp_qt = float(p.amount)
            tmp_tot = tmp_prix*tmp_qt
            total_ht += tmp_tot
            pdf.set_fill_color(255, 255, 255)
            pdf.cell(10)
            pdf.cell(80, 11, str(p.description), ln=0, border="L")
            pdf.cell(30, 11, str(p.amount), ln=0, border="L")
            pdf.cell(30, 11, str(p.price_ht)+' €', ln=0, border="L")
            pdf.cell(30, 11, str(tmp_tot) + ' €', ln=1, border="LR")
        
        pdf.cell(10, 11, '', ln=0)
        pdf.cell(80, 11, '', ln=0, border="T")
        pdf.cell(60, 11, 'Total H.TVA', ln=0, border=bd)
        pdf.cell(30, 11, str(total_ht)+' €', ln=1, border=bd)
        tva = total_ht * float(bill.tva_rate)
        pdf.cell(90, 11, '', ln=0)
        pdf.cell(60, 11, 'TVA ' + str(int(bill.tva_rate*100))+'%', ln=0, border=bd)
        pdf.cell(30, 11, str(tva) + ' €', ln=1, border=bd)
        
        pdf.cell(90, 12, '', ln=0)
        pdf.cell(60, 11, 'Total TTC EUR', ln=0, border=bd)
        pdf.cell(30, 11, str(total_ht+tva)+' €', ln=1, border=bd)
        
        pdf.cell(90, 5, '', ln=1)
        pdf.cell(10, 11, '', ln=0)
        pdf.set_font('Times_New_Roman', "", 11)
        pdf.cell(30, 11, 'Compte bancaire :', ln=0)
        pdf.set_font('Times_New_RomanB', "B", 11)
        pdf.cell(25, 11, company.iban, ln=1)
        
        pdf.cell(10, 11, '', ln=0)
        pdf.set_font('Times_New_Roman', "", 11)
        pdf.cell(30, 11, 'Certifié sincère et véritable', ln=1)
        
        pdf.cell(10, 11, '', ln=0)
        pdf.set_font('Times_New_RomanB', "B", 11)
        pdf.cell(30, 11, 'Veuillez mentionner la référence de la facture en communication lors du paiement.', ln=1)
        pdf.output(bill.num_ref+'.pdf')
