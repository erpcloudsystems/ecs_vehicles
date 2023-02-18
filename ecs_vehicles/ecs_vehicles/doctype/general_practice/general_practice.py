# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GeneralPractice(Document):
	def validate(self):
		general_practise_list = frappe.db.sql(""" Select general_practice_no from `tabGeneral Practice`
		where fiscal_year = '{fiscal_year}' and name != '{name}' """.format(name=self.name,
																			fiscal_year=self.fiscal_year), as_dict=1)

		for x in general_practise_list:
			if self.general_practice_no == x.general_practice_no:
				frappe.throw(
					" لا يمكن إستخدام رقم الممارسة العامة " + str(x.general_practice_no) + " أكثر من مرة ")

		general_practice_no = self.general_practice_no
		new_fiscal_year = self.fiscal_year
		self.document_name = "ممارسة عامة " + "(" + str(general_practice_no) + ")" + " لسنة " + str(new_fiscal_year)
