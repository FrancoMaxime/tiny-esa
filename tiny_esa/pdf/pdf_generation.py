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
import datetime

class HTML2PDF(FPDF):
    def header(self):
        # Set up a logo
        self.image('lnsc.png', 20, 8, 60)
        self.set_font('Times_New_Roman',"", 9)
        self.set_text_color(31, 59, 115)
        # Add an address
        self.cell(100)
        self.cell(45, 5 , '4, Chemin de la garde', ln=0)
        self.cell(45, 5, 'GSM : 0493/825038', ln=1)
        self.cell(100)
        self.cell(45, 5, '7040 Quévy-le-Petit', ln=0)
        self.cell(45, 5, 'Tél : 065/363346', ln=1)
        self.cell(145)
        self.cell(45, 5, 'Email : ln-sc@outlook.com', ln=1)
        
        # Line break
        self.ln(20)
 
    def footer(self):
        self.set_y(-17)
        self.set_font('Times_New_Roman',"", 9)
        self.set_text_color(31, 59, 115)
        self.set_draw_color(31, 59, 115)
        self.line(30, 275, 180, 275)
        self.cell(25)
        self.cell(50, 5 , 'TVA: BE 0679 835 980', ln=0)
        self.cell(60, 5 , 'IBAN: BE85 7512 0877 9406', ln=0)
        self.cell(50, 5, 'BIC: AXABBE22', ln=1)
        
    def generate(self, facture):
        bd = "LTRB"
        pdf = HTML2PDF()
        pdf.add_font('Times_New_Roman', '', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf', uni=True)
        pdf.add_font('Times_New_RomanB', 'B', '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.ttf', uni=True)
        pdf.set_font('Times_New_RomanB',"B", 20)
        pdf.set_title("Facture")
        pdf.set_author('Lionel Navez')
        pdf.add_page()
        
        pdf.set_font('Times_New_RomanB',"B", 20)
        pdf.cell(10)
        pdf.cell(100, 20 , 'FACTURE', ln=0)
        pdf.set_line_width(0.5)
        pdf.cell(70, 20 , facture.facture_id.get() , ln=1, border=bd, align="C")
        
        pdf.set_line_width(0.4)
        pdf.set_font('Times_New_RomanB',"B", 12)
        pdf.cell(10)
        pdf.cell(100, 20 , 'N/REF : '+ str(facture.ref_id.get()), ln=1)
        
        pdf.set_font('Times_New_Roman',"", 11)
        pdf.cell(10)
        pdf.cell(60, 12 , 'Date de facturation', ln=0, border=bd, align="C")
        pdf.cell(60, 12 , 'Echéance', ln=1, border=bd, align="C")
        pdf.cell(10)
        pdf.cell(60, 10, str(facture.date_fact.get()), ln=0, border=bd, align="C")
        pdf.cell(60, 10, str(facture.date_echeance.get()), ln=1, border=bd, align="C")
        
        pdf.cell(10,5,'',ln=1)
        pdf.cell(10)
        pdf.set_fill_color(192, 192, 192)
        pdf.cell(80, 12 , 'Description', ln=0, border=bd, align="C", fill = True)
        pdf.cell(30, 12 , 'Quantité', ln=0, border=bd, align="C", fill = True)
        pdf.cell(30, 12 , 'PU HT', ln=0, border=bd, align="C", fill = True)
        pdf.cell(30, 12 , 'Total HT EUR', ln=1, border=bd, align="C", fill = True)
        total_ht = 0
        for e in self.elements:
            tmp_prix = float(e[2].get())
            tmp_qt = float(e[1].get())
            tmp_tot = tmp_prix*tmp_qt
            total_ht +=tmp_tot
            pdf.set_fill_color(255, 255, 255)
            pdf.cell(10)
            pdf.cell(80, 11 , str(e[0].get()), ln=0, border="L")
            pdf.cell(30, 11 , str(e[1].get()), ln=0, border="L")
            pdf.cell(30, 11 , str(e[2].get())+' €', ln=0, border="L" )
            pdf.cell(30, 11 , str(tmp_tot) + ' €', ln=1, border="LR")
        
        pdf.cell(10,11,'',ln=0)
        pdf.cell(80, 11 , '', ln=0, border="T")
        pdf.cell(60, 11 , 'Total H.TVA', ln=0, border=bd )
        pdf.cell(30, 11 , str(total_ht)+' €', ln=1, border=bd)
        tva = total_ht*self.tva_value.get()
        pdf.cell(90, 11 , '', ln=0)
        pdf.cell(60, 11 , 'TVA ' +str(int(facture.tva_value.get()*100))+'%', ln=0, border=bd )
        pdf.cell(30, 11 , str(tva) + ' €', ln=1, border=bd)
        
        pdf.cell(90, 12 , '', ln=0)
        pdf.cell(60, 11, 'Total TTC EUR', ln=0, border=bd )
        pdf.cell(30, 11 , str(total_ht+tva)+' €', ln=1, border=bd)
        
        pdf.cell(90, 5 , '', ln=1)
        pdf.cell(10,11,'',ln=0)
        pdf.set_font('Times_New_Roman',"", 11)
        pdf.cell(30, 11 , 'Compte bancaire :', ln=0)
        pdf.set_font('Times_New_RomanB',"B", 11)
        pdf.cell(25, 11 , 'BE85 7512 0877 9406', ln=1)
        
        pdf.cell(10,11,'',ln=0)
        pdf.set_font('Times_New_Roman',"", 11)
        pdf.cell(30, 11 , 'Certifié sincère et véritable', ln=1)
        
        pdf.cell(10,11,'',ln=0)
        pdf.set_font('Times_New_RomanB',"B", 11)
        pdf.cell(30, 11 , 'Veuillez mentionner la référence de la facture en communication lors du paiement.', ln=1)
        pdf.output(self.facture_id.get()+'.pdf')
