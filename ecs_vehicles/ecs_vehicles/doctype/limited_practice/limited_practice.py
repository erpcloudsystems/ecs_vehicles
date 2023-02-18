# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LimitedPractice(Document):
	def validate(self):
		limited_practise_list = frappe.db.sql(""" Select limited_practice_no from `tabLimited Practice`
		where fiscal_year = '{fiscal_year}' and name != '{name}' """.format(name=self.name,
																			fiscal_year=self.fiscal_year), as_dict=1)

		for x in limited_practise_list:
			if self.limited_practice_no == x.limited_practice_no:
				frappe.throw(
					" لا يمكن إستخدام رقم الممارسة المحدودة " + str(x.limited_practice_no) + " أكثر من مرة ")

		limited_practice_no = self.limited_practice_no
		new_fiscal_year = self.fiscal_year
		self.document_name = "ممارسة محدودة " + "(" + str(limited_practice_no) + ")" + " لسنة " + str(new_fiscal_year)
